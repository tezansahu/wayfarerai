import argparse
from pyfiglet import Figlet
from termcolor import colored

import agent

def parse_args():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Wayfarer AI')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--memory_window', dest='memory_window', type=int, help='Set the rolling window size of the chat history', default=5)
    return parser.parse_args()

def print_ascii_art():
    # Print ASCII art
    f = Figlet(font='slant')
    ascii_art = f.renderText('Wayfarer AI')
    colored_ascii_art = colored(ascii_art, 'cyan', attrs=['bold'])
    print(colored_ascii_art)

def main():
    args = parse_args()
    print_ascii_art()

    # Set up agent with optional arguments
    wayfarer_ai_agent = agent.WayfarerAIAgent(debug=args.debug, memory_window=args.memory_window)
    wayfarer_ai_agent.chat()

if __name__ == "__main__":
    main()