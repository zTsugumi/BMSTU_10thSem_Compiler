; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"cmp"(i32 %"a", i32 %"b") 
{
entry:
  %"a.1" = alloca i32
  store i32 %"a", i32* %"a.1"
  %"b.1" = alloca i32
  store i32 %"b", i32* %"b.1"
  %".6" = load i32, i32* %"a.1"
  %".7" = load i32, i32* %"b.1"
  %".8" = icmp slt i32 %".6", %".7"
  %".9" = sext i1 %".8" to i32
  ret i32 %".9"
}

define i32 @"main"() 
{
entry:
  %"a" = alloca i32
  store i32 10, i32* %"a"
  %"b" = alloca i32
  store i32 30, i32* %"b"
  %".4" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".5" = load i32, i32* %"a"
  %".6" = load i32, i32* %"b"
  %".7" = call i32 @"cmp"(i32 %".5", i32 %".6")
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".7")
  ret i32 0
}

@".str0" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...) 

