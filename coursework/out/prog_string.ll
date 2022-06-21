; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"str" = alloca i8*
  %".2" = getelementptr inbounds [4 x i8], [4 x i8]* @".str0", i32 0, i32 0
  store i8* %".2", i8** %"str"
  %".4" = getelementptr inbounds [3 x i8], [3 x i8]* @".str1", i32 0, i32 0
  %".5" = load i8*, i8** %"str"
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".4", i8* %".5")
  ret i32 0
}

@".str0" = constant [4 x i8] c"abc\00"
@".str1" = constant [3 x i8] c"%s\00"
declare i32 @"printf"(i8* %".1", ...) 

