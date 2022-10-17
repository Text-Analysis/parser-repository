from parser import ParserRepo
import pprint

parser_repo = ParserRepo('Text-Analysis', 'srsparser')
pprint.pprint(parser_repo.get_data())
