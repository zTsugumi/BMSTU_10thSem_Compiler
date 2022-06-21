; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"ch" = alloca i8
  store i8 97, i8* %"ch"
  %".3" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".4" = load i8, i8* %"ch"
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".3", i8 %".4")
  ret i32 0
}

@".str0" = constant [3 x i8] c"%c\00"
declare i32 @"printf"(i8* %".1", ...) 

