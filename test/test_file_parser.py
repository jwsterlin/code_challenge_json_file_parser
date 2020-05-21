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

    def file_matches_contents(self, file_to_check, expected_contents):
        with open(file_to_check, "r") as output_file:
            lines = [x.rstrip() for x in output_file.readlines()]
            file_content = "\n".join(lines)
        self.maxDiff = None
        self.assertEqual(file_content, expected_contents)

    def test_full_parse_file(self):
        input_file_loc = "input_files/23222DSR.txt"
        output_file_loc = f"{TEST_WORK_DIR}/23222DSR.csv"

        fp = FileParser()
        fp.parse_file(input_file_loc, output_file_loc)
        self.assertTrue(os.path.exists(output_file_loc), "Output csv file was created")

        expected_contents = """Rashawn,Goldner,Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.,2013-02-07T16:10:14.117-06:00
Kira,Kertzmann,Vel incidunt eos deleniti earum. Velit doloribus ipsa deserunt. Omnis sed sed.,2013-02-07T16:10:14.268-06:00
Aurelia,Beahan,Id est atque sint. Et ratione nihil dolores inventore. Officia non et qui aut et voluptas eos. Cum quis quibusdam est.,2013-02-07T16:10:14.422-06:00
Kylie,Schinner,Quo ut pariatur. Assumenda consequatur quaerat sint at maiores autem.,2013-02-07T16:10:14.576-06:00
Nia,Crona,Doloremque eaque eligendi quia temporibus omnis rerum veritatis. In et expedita natus alias explicabo omnis sint.,2013-02-07T16:10:14.726-06:00
Keyon,Medhurst,Sit molestias sunt. Qui vel in. Voluptatem odit quaerat accusantium consequatur eos qui. Incidunt dolores sequi.,2013-02-07T16:10:14.888-06:00
Marco,Crooks,Similique voluptatibus corporis. In sunt hic odio est nemo temporibus at.,2013-02-07T16:10:15.040-06:00
Vallie,Bahringer,Hic sapiente aliquid dolorem et. Architecto beatae consectetur fugiat impedit nisi. Hic veritatis officiis tenetur sit.,2013-02-07T16:10:15.192-06:00
Bennett,Schuppe,Omnis omnis aut veniam molestiae nisi. Odio ea vitae unde non dolores. Omnis ipsum quae.,2013-02-07T16:10:15.344-06:00
Kieran,Beatty,In ipsam veritatis tempora occaecati quis corrupti. Eos quis adipisci provident autem minus asperiores quaerat.,2013-02-07T16:10:15.510-06:00"""
        self.file_matches_contents(output_file_loc, expected_contents)

    def test_combine_csvs(self):
        output_file_loc = f"{TEST_WORK_DIR}/output.csv"
        fp = FileParser()
        fp.parse_file("input_files/23222DSR.txt", f"{TEST_WORK_DIR}/23222DSR.csv")
        fp.parse_file("input_files/AJAFW79D.txt", f"{TEST_WORK_DIR}/AJAFW79D.csv")
        fp.combine_csvs(
            [f"{TEST_WORK_DIR}/23222DSR.csv", f"{TEST_WORK_DIR}/AJAFW79D.csv"],
            output_file_loc
        )
        self.assertTrue(os.path.exists(output_file_loc), "Combined output csv file was created")

        expected_contents = """Rashawn,Goldner,Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.,2013-02-07T16:10:14.117-06:00
Kira,Kertzmann,Vel incidunt eos deleniti earum. Velit doloribus ipsa deserunt. Omnis sed sed.,2013-02-07T16:10:14.268-06:00
Aurelia,Beahan,Id est atque sint. Et ratione nihil dolores inventore. Officia non et qui aut et voluptas eos. Cum quis quibusdam est.,2013-02-07T16:10:14.422-06:00
Kylie,Schinner,Quo ut pariatur. Assumenda consequatur quaerat sint at maiores autem.,2013-02-07T16:10:14.576-06:00
Nia,Crona,Doloremque eaque eligendi quia temporibus omnis rerum veritatis. In et expedita natus alias explicabo omnis sint.,2013-02-07T16:10:14.726-06:00
Keyon,Medhurst,Sit molestias sunt. Qui vel in. Voluptatem odit quaerat accusantium consequatur eos qui. Incidunt dolores sequi.,2013-02-07T16:10:14.888-06:00
Marco,Crooks,Similique voluptatibus corporis. In sunt hic odio est nemo temporibus at.,2013-02-07T16:10:15.040-06:00
Vallie,Bahringer,Hic sapiente aliquid dolorem et. Architecto beatae consectetur fugiat impedit nisi. Hic veritatis officiis tenetur sit.,2013-02-07T16:10:15.192-06:00
Bennett,Schuppe,Omnis omnis aut veniam molestiae nisi. Odio ea vitae unde non dolores. Omnis ipsum quae.,2013-02-07T16:10:15.344-06:00
Kieran,Beatty,In ipsam veritatis tempora occaecati quis corrupti. Eos quis adipisci provident autem minus asperiores quaerat.,2013-02-07T16:10:15.510-06:00
Talia,Kunde,Ullam voluptatibus eius reiciendis. Corporis eaque eum ducimus quidem voluptatem cupiditate. Voluptatem nulla quibusdam aliquam in earum assumenda. Aliquid corporis consequuntur aut quam sit quas.,2013-02-07T16:10:15.683-06:00
Taurean,Franecki,Perferendis totam quidem earum. Cum accusantium sunt aliquid. Similique qui non molestias. Aut adipisci unde.,2013-02-07T16:10:15.841-06:00
Alysa,Anderson,Sunt quas nisi tenetur corrupti in recusandae. Labore rem atque.,2013-02-07T16:10:15.993-06:00
Sonny,Steuber,Tempore sequi rerum ea. Consequuntur nihil expedita sunt accusamus. Autem voluptas ab repudiandae quis.,2013-02-07T16:10:16.142-06:00
Adrienne,Fisher,Laborum non quia ullam fuga vel. Nemo eaque impedit veritatis unde eos.,2013-02-07T16:10:16.292-06:00
Nikolas,Wilkinson,Ea quia fuga eos quae. Beatae aliquid ratione. Nisi commodi repudiandae.,2013-02-07T16:10:16.447-06:00
Jimmy,Romaguera,Et sed totam. Laboriosam quia explicabo quia minus rerum. Sed dolorem vel pariatur. Maxime delectus veniam omnis dignissimos minima.,2013-02-07T16:10:16.596-06:00
Christelle,Franecki,Sit alias sit incidunt dolores id. Quam ex est perspiciatis odit.,2013-02-07T16:10:16.746-06:00
Linwood,Kuhn,Perferendis perspiciatis tempore ipsam non sed. Tempora sed et. Velit qui omnis ipsam et. Commodi eligendi odio aut.,2013-02-07T16:10:16.900-06:00
Clementina,Bayer,Cupiditate vitae unde similique. Eaque quaerat et autem minima maiores. Aut voluptatem saepe id dicta et impedit. Magni nesciunt aut sit minima debitis iusto.,2013-02-07T16:10:17.063-06:00"""
        self.file_matches_contents(output_file_loc, expected_contents)