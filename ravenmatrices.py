import json
import pycurl
import argparse

optimal  = "a:1-4 a:2-5 a:3-1 a:4-2 a:5-6 a:6-3 a:7-6 a:8-2 a:9-1 a:10-3 a:11-4 a:12-5 b:1-5 b:2-6 b:3-2 b:4-1 b:5-1 b:6-3 b:7-5 b:8-6 b:9-4 b:10-3 b:11-4 b:12-8 c:1-5 c:2-3 c:3-2 c:4-7 c:5-8 c:6-4 c:7-5 c:8-7 c:9-1 c:10-1 c:11-6 c:12-2 d:1-3 d:2-4 d:3-3 d:4-8 d:5-7 d:6-6 d:7-5 d:8-4 d:9-1 d:10-2 d:11-5 d:12-6 e:1-7 e:2-6 e:3-8 e:4-2 e:5-1 e:6-5 e:7-1 e:8-3 e:9-6 e:10-2 e:11-4 e:12-5"
base = "a:1-3 a:2-5 a:3-1 a:4-5 a:5-5 a:6-3 a:7-2 a:8-1 a:9-8 a:10-4 a:11-2 a:12-5 b:1-5 b:2-5 b:3-7 b:4-4 b:5-1 b:6-1 b:7-2 b:8-6 b:9-6 b:10-3 b:11-2 b:12-2 c:1-7 c:2-2 c:3-2 c:4-4 c:5-4 c:6-7 c:7-2 c:8-5 c:9-1 c:10-2 c:11-1 c:12-7 d:1-1 d:2-2 d:3-8 d:4-8 d:5-7 d:6-5 d:7-1 d:8-8 d:9-3 d:10-2 d:11-8 d:12-1 e:1-7 e:2-2 e:3-6 e:4-4 e:5-8 e:6-6 e:7-2 e:8-2 e:9-5 e:10-1 e:11-3 e:12-5"

def cli_arg_parser():
  '''
    Setup argparse
  '''
  parser = argparse.ArgumentParser(
    description = "Raven matrices iq test bruteforce"
  )
  parser.add_argument(
    '-o',
    '--optimal',
    action='store_true',
    help='Do not bruteforce, instead use the precalculated solution'
  )
  parser.add_argument(
    '-b',
    '--bruteforce',
    action='store_true',
    default=True,
    help='Find optimal solution by educated guessing'
  )
  return parser.parse_args()

def query(data):
  '''
    Sends an answer file to the psycho-tests ajax endpoint and returns the "measured" IQ.
  '''
  c = pycurl.Curl()

  age = "56"
  fin = "1"
  url = "https://psycho-tests.com/ajaxtest9"
  req = "balls={}&year={}&finish={}".format(data,age,fin)
  headers = [
    'Accept: application/json, text/javascript, */*; q=0.01',
    'Accept-Language: en-US,en;q=0.5',
    'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Content-Type: application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With: XMLHttpRequest',
    'Origin: https://psycho-tests.com',
    'DNT: 1',
    'Pragma: no-cache',
    'Connection: keep-alive',
    'Referer: https://psycho-tests.com/test/raven-matrixes-test',
  ]

  c.setopt(pycurl.URL,url)
  c.setopt(pycurl.HTTPHEADER, headers)
  c.setopt(pycurl.POST, 1)
  c.setopt(pycurl.VERBOSE, 0)
  c.setopt(pycurl.POSTFIELDS, req)

  res = json.loads(c.perform_rs())
  c.close()

  return res

def init_answers():
  '''
    Generates an answer object with at least 12 correct answers, since everything below 12
    is considered an IQ of 35. The baseline string contains 12 correct answers and achieves an IQ of 62.
  '''
  answers = dict()
  baseline = "3 5 1 7 5 3 2 1 8 4 2 5 5 5 7 4 1 1 2 6 6 3 2 2 7 2 2 4 4 7 2 5 1 2 1 7 1 2 8 8 7 5 1 8 3 2 8 1 7 2 6 4 8 6 2 2 5 1 3 5"
  for k,i in enumerate(["a", "b", "c", "d", "e"]):
    for j in range(1,13):
      answers["{}:{}".format(i, j)] = baseline.split(' ')[k*12+j-1]
  return answers

def answer_dict_to_str(answers):
  '''
    Converts an answer object to a string format the API understands.
  '''
  tmp = str()
  for key in answers:
    tmp += "{}-{} ".format(key,str(answers[key]))
  return tmp

def maximize_iq():
  '''
    Figure out right answers by trying out stuff and watching for changes in the IQ response.
    Returns an optimal set of answers.
  '''
  iq_old = 0
  aw = init_answers()
  for i in aw:
    aw_new = init_answers()
    print("{}".format(i))
    for j in range(1, 9):
      aw_new[i]=j
      iq = query(answer_dict_to_str(aw_new))["iq"]
      if iq >= iq_old:
        iq_old = iq;
        aw[i] = j
      print("\t{}->{}".format(j, iq))
    print("\tpicked {}".format(aw[i]))
  return aw

if __name__ == '__main__':
  '''
    I don't know why I created this ...
  '''
  args = cli_arg_parser()
  if args.optimal:
    ret = query(optimal)
  else:
    print("Figuring out stuff...")
    solution = maximize_iq()
    optimal = answer_dict_to_str(solution)
    ret = query(optimal)
  print("Found optimal solution:\n\nOptimal: {}\n\nIQ: {}\n\nMessage: {}\n".format(optimal, ret["iq"], ret["str"]))
