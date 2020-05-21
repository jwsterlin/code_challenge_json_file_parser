import unittest
import os
import shutil

from file_parser.file_parser import FileParser

TEST_WORK_DIR = "tst_wrk_dir"

class TestFileParser(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir(TEST_WORK_DIR)
        except OSError as e:
            print(f"Creation of test work directory {TEST_WORK_DIR} failed: {e}")

    def tearDown(self):
        try:
            shutil.rmtree(TEST_WORK_DIR, ignore_errors=True)
        except Exception as e:
            print(f"Removal of test work directory {TEST_WORK_DIR} failed: {e}")

    def test_full_parse_file(self):
        input_file_loc = "input_files/23222DSR.txt"
        output_file_loc = f"{TEST_WORK_DIR}/23222DSR.csv"

        fp = FileParser()
        fp.parse_file(input_file_loc, output_file_loc)
        self.assertTrue(os.path.exists(output_file_loc), "Output csv file was created")

        with open(output_file_loc, "r") as output_file:
            lines = [x.rstrip() for x in output_file.readlines()]
            content = "\n".join(lines)

        self.maxDiff = None
        self.assertEqual(
            content,
            """Rashawn,Goldner,Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.,2013-02-07T16:10:14.117-06:00
Kira,Kertzmann,Vel incidunt eos deleniti earum. Velit doloribus ipsa deserunt. Omnis sed sed.,2013-02-07T16:10:14.268-06:00
Aurelia,Beahan,Id est atque sint. Et ratione nihil dolores inventore. Officia non et qui aut et voluptas eos. Cum quis quibusdam est.,2013-02-07T16:10:14.422-06:00
Kylie,Schinner,Quo ut pariatur. Assumenda consequatur quaerat sint at maiores autem.,2013-02-07T16:10:14.576-06:00
Nia,Crona,Doloremque eaque eligendi quia temporibus omnis rerum veritatis. In et expedita natus alias explicabo omnis sint.,2013-02-07T16:10:14.726-06:00
Keyon,Medhurst,Sit molestias sunt. Qui vel in. Voluptatem odit quaerat accusantium consequatur eos qui. Incidunt dolores sequi.,2013-02-07T16:10:14.888-06:00
Marco,Crooks,Similique voluptatibus corporis. In sunt hic odio est nemo temporibus at.,2013-02-07T16:10:15.040-06:00
Vallie,Bahringer,Hic sapiente aliquid dolorem et. Architecto beatae consectetur fugiat impedit nisi. Hic veritatis officiis tenetur sit.,2013-02-07T16:10:15.192-06:00
Bennett,Schuppe,Omnis omnis aut veniam molestiae nisi. Odio ea vitae unde non dolores. Omnis ipsum quae.,2013-02-07T16:10:15.344-06:00
Kieran,Beatty,In ipsam veritatis tempora occaecati quis corrupti. Eos quis adipisci provident autem minus asperiores quaerat.,2013-02-07T16:10:15.510-06:00"""
        )