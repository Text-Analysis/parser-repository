from parser import ParserRepo
import pprint

parser_repo = ParserRepo('Text-Analysis', 'doc-gost-api')
pprint.pprint(parser_repo.get_data())
