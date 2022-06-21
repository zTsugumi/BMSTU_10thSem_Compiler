; ModuleID = "C Compiler"

%"S" = type {i32}
define i32 @"main"()
{
entry:
  %"a" = alloca %"S"
  %"b" = alloca %"S"*
  %".2" = getelementptr inbounds %"S", %"S"* %"a", i32 0, i32 0
  store i32 1, i32* %".2"
  %".4" = load %"S"*, %"S"** %"b"
  %".5" = getelementptr inbounds %"S", %"S"* %".4", i32 0, i32 0
  store i32 2, i32* %".5"
  %".7" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".8" = getelementptr inbounds %"S", %"S"* %"a", i32 0, i32 0
  %".9" = load i32, i32* %".8"
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".9")
  %".11" = getelementptr inbounds [3 x i8], [3 x i8]* @".str1", i32 0, i32 0
  %".12" = load %"S"*, %"S"** %"b"
  %".13" = getelementptr inbounds %"S", %"S"* %".12", i32 0, i32 0
  %".14" = load i32, i32* %".13"
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".11", i32 %".14")
  ret i32 0
}

@".str0" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...)

@".str1" = constant [3 x i8] c"%d\00"
