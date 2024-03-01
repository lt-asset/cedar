import argparse
import datetime
def time_elapsed(h1,m1,s1, h2, m2, s2): 
    time_1 = datetime.timedelta(hours=int(h1), minutes=int(m1), seconds=int(s1))
    time_2 = datetime.timedelta(hours=int(h2), minutes=int(m2), seconds=int(s2))

    time_interval = time_2 - time_1
    print(time_interval)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('h1')
    parser.add_argument('m1')
    parser.add_argument('s1')
    parser.add_argument('h2')
    parser.add_argument('m2')
    parser.add_argument('s2')

    args = parser.parse_args()
    time_elapsed(args.h1, args.m1, args.s1, args.h2, args.m2, args.s2)
