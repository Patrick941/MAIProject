from compare50 import passes
import compare50
"""
Compares scored submission pairs more granularly.

:param scores: Scored submission pairs to be compared more granularly.
:type scores: list of compare50.Score
:param ignored_files: Files containing distro code.
:type ignored_files: set of compare50.File
:param pass_: Pass whose comparator should be used to compare the submissions.
:type pass_: compare50.Pass
:returns: Compare50Results corresponding to each of the given scores.
:rtype: list of compare50.Compare50Result

Performs an in-depth comparison of each submission pair and returns a corresponding
list of compare50.Compare50Results.
"""

sub1 = compare50.Submission("artifacts", files=["output_0.py"])
sub2 = compare50.Submission("artifacts", files=["output_1.py"])
score = compare50.Score(sub1, sub2, 1.0)
result = compare50.compare([score], ignored_files=set(), pass_=passes.structure())

print(result)
