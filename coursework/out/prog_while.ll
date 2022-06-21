; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %".3"
.3:
  %".7" = load i32, i32* %"i"
  %".8" = icmp sle i32 %".7", 10
  %".9" = icmp ne i1 %".8", 0
  br i1 %".9", label %".4", label %".5"
.4:
  %".11" = load i32, i32* %"i"
  %".12" = add i32 %".11", 2
  store i32 %".12", i32* %"i"
  %".14" = getelementptr inbounds [4 x i8], [4 x i8]* @".str0", i32 0, i32 0
  %".15" = load i32, i32* %"i"
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".14", i32 %".15")
  br label %".3"
.5:
  ret i32 0
}

@".str0" = constant [4 x i8] c"%d \00"
declare i32 @"printf"(i8* %".1", ...) 

