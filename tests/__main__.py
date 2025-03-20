from tests.file_test import *
from tests.sql_test import *


TEST_CASE = 2

def test_main():
  match TEST_CASE:
    case 0:
      file_test()
      sql_test()
      return
    case 1:
      file_test()
      return
    case 2:
      sql_test()
      return


if __name__ == "__main__":
  test_main()