; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = global [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5]
define i32 @"main"() 
{
entry:
  %"b" = alloca [5 x i32]
  store [5 x i32] [i32 5, i32 4, i32 3, i32 2, i32 1], [5 x i32]* %"b"
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %".4"
.4:
  %".8" = load i32, i32* %"i"
  %".9" = icmp sle i32 %".8", 4
  %".10" = icmp ne i1 %".9", 0
  br i1 %".10", label %".5", label %".6"
.5:
  %"c" = alloca i32
  %".12" = load i32, i32* %"i"
  %".13" = getelementptr inbounds [5 x i32], [5 x i32]* @"a", i32 0, i32 %".12"
  %".14" = load i32, i32* %".13"
  %".15" = load i32, i32* %"i"
  %".16" = getelementptr inbounds [5 x i32], [5 x i32]* %"b", i32 0, i32 %".15"
  %".17" = load i32, i32* %".16"
  %".18" = sub i32 %".14", %".17"
  store i32 %".18", i32* %"c"
  %".20" = getelementptr inbounds [4 x i8], [4 x i8]* @".str1", i32 0, i32 0
  %".21" = load i32, i32* %"c"
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".20", i32 %".21")
  %".23" = load i32, i32* %"i"
  %".24" = add i32 %".23", 1
  store i32 %".24", i32* %"i"
  br label %".4"
.6:
  ret i32 0
}

@".str1" = constant [4 x i8] c"%d \00"
declare i32 @"printf"(i8* %".1", ...) 

