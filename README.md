# ravenmatrices

"Smart" bruteforcer for a silly online iq test. It's absolutely useless, the test
is garbage, but it was fun.

# usage

```bash
usage: pyquiz.py [-h] [-o] [-b]

Raven matrices iq test bruteforce

optional arguments:
  -h, --help        show this help message and exit
  -o, --optimal     Do not bruteforce, instead use the precalculated solution
  -b, --bruteforce  Find optimal solution by educated guessing
```

# what?

Finds the highest rated solution for the [raven-matrices](https://psycho-tests.com/test/raven-matrixes-test) iq test.

# why?

I don't know.

# how?

There are 60 questions, a result below 12 correct answered questions is somehow
considered an IQ of 35. So I determined a baseline solution that gets the
lowest possible IQ without dropping to 35. This happens to be 62 for some
reasons. The script just tries each possible solution for each question
and monitors the resulting IQ. A correct answer increases the result as there
is only one correct answer in each set of questions. Which means the script
plays 8*60 quizes and tortures the ajax api. This is fine.
