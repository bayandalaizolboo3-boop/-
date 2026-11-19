import sys

def main():
  
  print("=== Python Exception Handling ===")

#Step 01: ZeroDivisionError
print("\n[Step 01] ZeroDivisionError")

try:
  v = 10 / 0
  print(v)

except ZeroDivisionError:
  print("0으로 나눌 수 없습니다!")

#Step 02: ValueError
print("\n[Step 02] ValueError")

try:
  v = int('abc')
  print(v)

except ValueError:
  print('정수 변환 실패!')

#Step 03: User input Test
print("\n[STEP 03] Input Test")

try:
  number = int(input("숫자를 입력하세요!")
  print("입력한 숫자:", number)

except ValueError:
  print("올바른 숫자를 입력하세요!")

#Step 04: Calculator
print("\n[Step 04] Simple Calculator")

try:
  a = int(input("첫 번재 숫자: "))
  b = int(input("두 번재 숫자: "))

  result = a / b
  print("계산 결과:", result)

except ValueError:
  print("올바른 숫자를 입력하세요!")

except ZeroDivisionEror:
  print("0으로 나눌 수 없습니다!")

if __name__ == "__main__":
  main()
