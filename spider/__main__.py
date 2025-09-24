from argparse import ArgumentParser

# The CARRIE Project

# CUNY
# Automated
# Research
# Indexer
# Explorer

def main():
    """
    """
    parser = ArgumentParser( prog="carrie",
                        description= "")
    
    parser.add_argument('site',
                        type=str,
                        help=''
                        )  # positional argument
    
    parser.add_argument('-o', '--output-file')

    parser.add_argument('-v', 
                        '--verbose', 
                        action='store_true',
                        help='''shows the background
                        events'''
                        )

    parser.add_argument('a', '--all')

    parser.add_argument('--query')

    parser.add_argument('-y', '--assume-yes')

