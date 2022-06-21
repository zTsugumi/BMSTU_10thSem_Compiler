; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"temp" = alloca i32
  store i32 10, i32* %"temp"
  %".3" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".4" = load i32, i32* %"temp"
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".3", i32 %".4")
  ret i32 0
}

@".str0" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...) 

