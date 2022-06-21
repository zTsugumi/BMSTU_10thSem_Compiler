; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"cmp"(i32* %"a", i32* %"b") 
{
entry:
  %"a.1" = alloca i32*
  store i32* %"a", i32** %"a.1"
  %"b.1" = alloca i32*
  store i32* %"b", i32** %"b.1"
  %".6" = load i32*, i32** %"a.1"
  %".7" = load i32*, i32** %"b.1"
  %".8" = load i32, i32* %".6"
  %".9" = load i32, i32* %".7"
  %".10" = sub i32 %".8", %".9"
  ret i32 %".10"
}

define i32 @"main"() 
{
entry:
  %"a" = alloca i32
  store i32 1, i32* %"a"
  %"b" = alloca i32
  store i32 2, i32* %"b"
  %".4" = getelementptr inbounds [4 x i8], [4 x i8]* @".str0", i32 0, i32 0
  %".5" = load i32, i32* %"a"
  %".6" = load i32, i32* %"b"
  %".7" = add i32 %".5", %".6"
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".7")
  %".9" = getelementptr inbounds [4 x i8], [4 x i8]* @".str1", i32 0, i32 0
  %".10" = load i32, i32* %"a"
  %".11" = load i32, i32* %"b"
  %".12" = sub i32 %".10", %".11"
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".12")
  %".14" = getelementptr inbounds [4 x i8], [4 x i8]* @".str2", i32 0, i32 0
  %".15" = load i32, i32* %"a"
  %".16" = load i32, i32* %"b"
  %".17" = mul i32 %".15", %".16"
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".14", i32 %".17")
  %".19" = getelementptr inbounds [4 x i8], [4 x i8]* @".str3", i32 0, i32 0
  %".20" = load i32, i32* %"a"
  %".21" = load i32, i32* %"b"
  %".22" = sdiv i32 %".20", %".21"
  %".23" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 %".22")
  %".24" = getelementptr inbounds [4 x i8], [4 x i8]* @".str4", i32 0, i32 0
  %".25" = load i32, i32* %"a"
  %".26" = load i32, i32* %"b"
  %".27" = srem i32 %".25", %".26"
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".24", i32 %".27")
  %".29" = getelementptr inbounds [4 x i8], [4 x i8]* @".str5", i32 0, i32 0
  %".30" = call i32 @"cmp"(i32* %"a", i32* %"b")
  %".31" = call i32 (i8*, ...) @"printf"(i8* %".29", i32 %".30")
  ret i32 0
}

@".str0" = constant [4 x i8] c"%d\0a\00"
declare i32 @"printf"(i8* %".1", ...) 

@".str1" = constant [4 x i8] c"%d\0a\00"
@".str2" = constant [4 x i8] c"%d\0a\00"
@".str3" = constant [4 x i8] c"%d\0a\00"
@".str4" = constant [4 x i8] c"%d\0a\00"
@".str5" = constant [4 x i8] c"%d\0a\00"
