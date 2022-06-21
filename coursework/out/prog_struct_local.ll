; ModuleID = "C Compiler"

%"S" = type {i32}
%"R" = type {i32}
define i32 @"main"()
{
entry:
  %"my_r2" = alloca %"R"*
  %"my_r1" = alloca %"R"
  %"a" = alloca %"S"
  %"b" = alloca %"S"*
  %".2" = getelementptr inbounds %"S", %"S"* %"a", i32 0, i32 0
  store i32 1, i32* %".2"
  %".4" = load %"S"*, %"S"** %"b"
  %".5" = getelementptr inbounds %"S", %"S"* %".4", i32 0, i32 0
  store i32 2, i32* %".5"
  %".7" = getelementptr inbounds %"R", %"R"* %"my_r1", i32 0, i32 0
  store i32 3, i32* %".7"
  %".9" = load %"R"*, %"R"** %"my_r2"
  %".10" = getelementptr inbounds %"R", %"R"* %".9", i32 0, i32 0
  store i32 4, i32* %".10"
  %".12" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".13" = getelementptr inbounds %"S", %"S"* %"a", i32 0, i32 0
  %".14" = load i32, i32* %".13"
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".14")
  %".16" = getelementptr inbounds [3 x i8], [3 x i8]* @".str1", i32 0, i32 0
  %".17" = load %"S"*, %"S"** %"b"
  %".18" = getelementptr inbounds %"S", %"S"* %".17", i32 0, i32 0
  %".19" = load i32, i32* %".18"
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".16", i32 %".19")
  %".21" = getelementptr inbounds [3 x i8], [3 x i8]* @".str2", i32 0, i32 0
  %".22" = getelementptr inbounds %"R", %"R"* %"my_r1", i32 0, i32 0
  %".23" = load i32, i32* %".22"
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".21", i32 %".23")
  %".25" = getelementptr inbounds [3 x i8], [3 x i8]* @".str3", i32 0, i32 0
  %".26" = load %"R"*, %"R"** %"my_r2"
  %".27" = getelementptr inbounds %"R", %"R"* %".26", i32 0, i32 0
  %".28" = load i32, i32* %".27"
  %".29" = call i32 (i8*, ...) @"printf"(i8* %".25", i32 %".28")
  ret i32 0
}

@".str0" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...)

@".str1" = constant [3 x i8] c"%d\00"
@".str2" = constant [3 x i8] c"%d\00"
@".str3" = constant [3 x i8] c"%d\00"
