"""
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

# Default packages
import argparse
import csv
import hashlib
import inspect
import json
import logging
import os
import sys
import traceback

# Internal packages
from dexofuzzy.core.generator import GenerateDexofuzzy

# 3rd-party packages
if sys.platform == "win32":
    import dexofuzzy.bin as ssdeep
else:
    import ssdeep


class Command:
    """
    This class handles Dexofuzzy commands.
    """
    def __init__(self):
        self.args = None
        self.logger = None

    def console(self):
        """
        This function handles Dexofuzzy console.
        """
        parser = argparse.ArgumentParser(
                prog="dexofuzzy",
                description=("Dexofuzzy - Dalvik EXecutable Opcode Fuzzyhash"),
                add_help=True)

        parser.add_argument(
                    "-f", "--file", metavar="SAMPLE_FILENAME",
                    help="the sample to extract dexofuzzy")
        parser.add_argument(
                    "-d", "--directory", metavar="SAMPLE_DIRECTORY",
                    help="the directory of samples to extract dexofuzzy")

        parser.add_argument(
                    "-m", "--method-fuzzy", action="store_true",
                    help="extract the fuzzyhash based on method of the sample"
                    + "(must include the -f or -d option by default)")

        parser.add_argument(
                    "-g", "--clustering", metavar=("N", "M"), nargs=2, type=int,
                    help="N-Gram Tokenizer and M-Partial Matching clustering"
                    + " based on the sample's dexofuzzy "
                    + "(must include the -d option by default)")

        parser.add_argument(
                    "-s", "--score", metavar="DEXOFUZZY", nargs=2,
                    help="score the dexofuzzy of the sample")

        parser.add_argument(
                    "-c", "--csv", metavar="CSV_FILENAME",
                    help="output as CSV format")
        parser.add_argument(
                    "-j", "--json", metavar="JSON_FILENAME",
                    help="output as json format " +
                    "(include method fuzzy or clustering)")
        parser.add_argument(
                    "-l", "--error-log", metavar="LOG_FILENAME",
                    help="output the error log")

        if len(sys.argv) == 1:
            parser.print_help()
            return None

        self.args = parser.parse_args()
        dexofuzzy_list = []

        if self.args.score:
            print(self.__get_dexofuzzy_compare(self.args.score[0], self.args.score[1]))

        if self.args.directory:
            for result in self.__search_directory(self.args.directory):
                if result is not None:
                    print(f'{result["file_name"]},{result["file_sha256"]},'
                          f'{result["file_size"]},{result["dexohash"]},'
                          f'{result["dexofuzzy"]}')

                    if self.args.method_fuzzy:
                        print(json.dumps(result["method_fuzzy"], indent=4))

                    dexofuzzy_list.append(result)

        if self.args.file:
            result = self.__search_file(self.args.file)
            if result is not None:
                print(f'{result["file_name"]},{result["file_sha256"]},'
                      f'{result["file_size"]},{result["dexohash"]},'
                      f'{result["dexofuzzy"]}')

                if self.args.method_fuzzy:
                    print(json.dumps(result["method_fuzzy"], indent=4))

                dexofuzzy_list.append(result)

        if self.args.clustering:
            if not self.args.directory:
                print("must include the -d option by default")
                return None

            dexofuzzy_list = self.__clustering_dexofuzzy(dexofuzzy_list,
                                                         self.args.clustering[0],
                                                         self.args.clustering[1])
            print(json.dumps(dexofuzzy_list, indent=4))

        if self.args.csv:
            try:
                with open(self.args.csv, "w", encoding="UTF-8", newline="") as csv_file:
                    fieldnames = ["file_name", "file_sha256", "file_size",
                                  "dexohash", "dexofuzzy"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()

                    for output in dexofuzzy_list:
                        row = {}
                        row["file_name"] = output["file_name"]
                        row["file_sha256"] = output["file_sha256"]
                        row["file_size"] = output["file_size"]
                        row["dexohash"] = output["dexohash"]
                        row["dexofuzzy"] = output["dexofuzzy"]
                        writer.writerow(row)

            except IOError:
                print(f"{inspect.stack()[0][3]} : {traceback.format_exc()}")
                return False

        if self.args.json:
            try:
                with open(self.args.json, "w", encoding="UTF-8") as json_file:
                    json.dump(dexofuzzy_list, json_file, indent=4)

            except IOError:
                print(f"{inspect.stack()[0][3]} : {traceback.format_exc()}")
                return False

    def __log_dexofuzzy(self, message=None, file=None):
        if self.args.error_log:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=self.args.error_log,
                                level=logging.INFO,
                                format="%(message)s")
            if file:
                message = f"{message} : {str(file)}"
                self.logger.error(message)

            else:
                self.logger.error(message)

            self.logger.error("%s", traceback.format_exc())

    def __get_dexofuzzy_compare(self, dexofuzzy_1, dexofuzzy_2):
        try:
            return ssdeep.compare(dexofuzzy_1, dexofuzzy_2)

        except Exception:
            self.__log_dexofuzzy("Unable to compare dexofuzzy")
            return None

    def __search_directory(self, sample_dir):
        if os.path.isdir(sample_dir) is False:
            print("The directory not found")

        sample_path = os.path.join(os.getcwd(), sample_dir)
        for root, _, files in os.walk(sample_path):
            for file in files:
                file_path = os.path.join(root, file)
                yield self.__get_report(file_path)

    def __search_file(self, sample_file):
        if os.path.isfile(sample_file) is False:
            print("The file not found")

        return self.__get_report(sample_file)

    def __get_report(self, file_path):
        try:
            report = None
            generate_dexofuzzy = GenerateDexofuzzy()
            result = generate_dexofuzzy.get_dexofuzzy(file_path, self.args.method_fuzzy)

            if result is not None:
                report = {}
                report["file_name"] = file_path
                report["file_sha256"] = self.__get_sha256(file_path)
                report["file_size"] = self.__get_file_size(file_path)
                report["dexohash"] = result["dexohash"]
                report["dexofuzzy"] = result["dexofuzzy"]

                if self.args.method_fuzzy:
                    report["method_fuzzy"] = result["method_fuzzy"]

            return report

        except Exception:
            self.__log_dexofuzzy(message="Unable to generate dexofuzzy",
                                 file=file_path)
            return None

    def __get_sha256(self, file_path):
        if not os.path.exists(file_path):
            self.__log_dexofuzzy(message="The file not found", file=file_path)

        try:
            with open(file_path, "rb") as file:
                data = file.read()

            sha256 = hashlib.sha256(data).hexdigest()
            return sha256

        except IOError:
            self.__log_dexofuzzy(message="Unable to get sha256", file=file_path)
            return None

    def __get_file_size(self, file_path):
        try:
            statinfo = os.stat(file_path)
            file_size = int(statinfo.st_size)

            return str(file_size)

        except IOError:
            self.__log_dexofuzzy(
                            message="Unable to get file size", file=file_path)
            return None

    def __clustering_dexofuzzy(self, dexofuzzy_list, n_gram, m_partial_matching):
        try:
            sources = destinations = dexofuzzy_list
            for source in sources:
                source["clustering"] = []
                src_dexofuzzy = source["dexofuzzy"].split(":")[1]

                for destination in destinations:
                    dst_dexofuzzy = destination["dexofuzzy"].split(":")[1]
                    signature = self.__search_n_gram(src_dexofuzzy, dst_dexofuzzy,
                                                     int(n_gram),
                                                     int(m_partial_matching))
                    if signature:
                        clustering = {}
                        clustering["file_name"] = destination["file_name"]
                        clustering["file_sha256"] = destination["file_sha256"]
                        clustering["file_size"] = destination["file_size"]
                        clustering["dexohash"] = destination["dexohash"]
                        clustering["dexofuzzy"] = dst_dexofuzzy
                        clustering["signature"] = signature
                        source["clustering"].append(clustering)

            return sources

        except Exception:
            self.__log_dexofuzzy(message="Unable to cluster dexofuzzy")
            return None

    def __search_n_gram(self, dexofuzzy_1, dexofuzzy_2, n_gram, m_partial_matching):
        try:
            partial_matching = 0
            signature_list = []

            for i in range(len(dexofuzzy_2)):
                if len(dexofuzzy_2[i:i+n_gram]) == n_gram:
                    if dexofuzzy_2[i:i+n_gram] in dexofuzzy_1:
                        partial_matching += 1
                        signature_list.append(dexofuzzy_2[i:i+n_gram])

                        if partial_matching == m_partial_matching:
                            return signature_list

            return None

        except Exception:
            self.__log_dexofuzzy(message="Unable to search n-gram")
            return None
