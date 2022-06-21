; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"i" = alloca i32
  store i32 0, i32* %"i"
  %".3" = load i32, i32* %"i"
  %".4" = add i32 %".3", 1
  store i32 %".4", i32* %"i"
  %".6" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".7" = load i32, i32* %"i"
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 %".7")
  ret i32 0
}

@".str0" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...) 

