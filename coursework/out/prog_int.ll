; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"i1" = alloca i32
  %"i2" = alloca i32
  store i32 1ull, i32* %"i1"
  store i32 2l, i32* %"i2"
  %".4" = getelementptr inbounds [4 x i8], [4 x i8]* @".str0", i32 0, i32 0
  %".5" = load i32, i32* %"i1"
  %".6" = load i32, i32* %"i2"
  %".7" = add i32 %".5", %".6"
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".7")
  %".9" = getelementptr inbounds [4 x i8], [4 x i8]* @".str1", i32 0, i32 0
  %".10" = load i32, i32* %"i1"
  %".11" = load i32, i32* %"i2"
  %".12" = sdiv i32 %".10", %".11"
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".12")
  %".14" = getelementptr inbounds [4 x i8], [4 x i8]* @".str2", i32 0, i32 0
  %".15" = load i32, i32* %"i1"
  %".16" = load i32, i32* %"i2"
  %".17" = mul i32 %".15", %".16"
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".14", i32 %".17")
  %".19" = getelementptr inbounds [4 x i8], [4 x i8]* @".str3", i32 0, i32 0
  %".20" = load i32, i32* %"i2"
  %".21" = load i32, i32* %"i2"
  %".22" = sub i32 %".20", %".21"
  %".23" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 %".22")
  ret i32 0
}

@".str0" = constant [4 x i8] c"%d\0a\00"
declare i32 @"printf"(i8* %".1", ...) 

@".str1" = constant [4 x i8] c"%d\0a\00"
@".str2" = constant [4 x i8] c"%d\0a\00"
@".str3" = constant [4 x i8] c"%d\0a\00"
