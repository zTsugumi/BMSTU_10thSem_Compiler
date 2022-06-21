; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = global [8 x i32] [i32 5, i32 4, i32 3, i32 3, i32 4, i32 5, i32 1, i32 2]
define i32 @"main"() 
{
entry:
  %"temp" = alloca i32
  %"n" = alloca i32
  %"j" = alloca i32
  %"i" = alloca i32
  store i32 0, i32* %"i"
  store i32 8, i32* %"n"
  %".4" = getelementptr inbounds [14 x i8], [14 x i8]* @".str1", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4")
  br label %".6"
.6:
  %".10" = load i32, i32* %"i"
  %".11" = load i32, i32* %"n"
  %".12" = icmp slt i32 %".10", %".11"
  %".13" = icmp ne i1 %".12", 0
  br i1 %".13", label %".7", label %".8"
.7:
  %".15" = getelementptr inbounds [4 x i8], [4 x i8]* @".str2", i32 0, i32 0
  %".16" = load i32, i32* %"i"
  %".17" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".16"
  %".18" = load i32, i32* %".17"
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".15", i32 %".18")
  %".20" = load i32, i32* %"i"
  %".21" = add i32 %".20", 1
  store i32 %".21", i32* %"i"
  br label %".6"
.8:
  store i32 0, i32* %"i"
  br label %".25"
.25:
  %".29" = load i32, i32* %"i"
  %".30" = load i32, i32* %"n"
  %".31" = sub i32 %".30", 1
  %".32" = icmp slt i32 %".29", %".31"
  %".33" = icmp ne i1 %".32", 0
  br i1 %".33", label %".26", label %".27"
.26:
  %".35" = load i32, i32* %"i"
  %".36" = add i32 %".35", 1
  store i32 %".36", i32* %"j"
  br label %".38"
.27:
  store i32 0, i32* %"i"
  %".80" = getelementptr inbounds [14 x i8], [14 x i8]* @".str3", i32 0, i32 0
  %".81" = call i32 (i8*, ...) @"printf"(i8* %".80")
  br label %".82"
.38:
  %".42" = load i32, i32* %"j"
  %".43" = load i32, i32* %"n"
  %".44" = icmp slt i32 %".42", %".43"
  %".45" = icmp ne i1 %".44", 0
  br i1 %".45", label %".39", label %".40"
.39:
  %".47" = load i32, i32* %"i"
  %".48" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".47"
  %".49" = load i32, i32* %".48"
  %".50" = load i32, i32* %"j"
  %".51" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".50"
  %".52" = load i32, i32* %".51"
  %".53" = icmp sgt i32 %".49", %".52"
  %".54" = icmp ne i1 %".53", 0
  br i1 %".54", label %".39.if", label %".39.endif"
.40:
  %".75" = load i32, i32* %"i"
  %".76" = add i32 %".75", 1
  store i32 %".76", i32* %"i"
  br label %".25"
.39.if:
  %".56" = load i32, i32* %"i"
  %".57" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".56"
  %".58" = load i32, i32* %".57"
  store i32 %".58", i32* %"temp"
  %".60" = load i32, i32* %"i"
  %".61" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".60"
  %".62" = load i32, i32* %"j"
  %".63" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".62"
  %".64" = load i32, i32* %".63"
  store i32 %".64", i32* %".61"
  %".66" = load i32, i32* %"j"
  %".67" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".66"
  %".68" = load i32, i32* %"temp"
  store i32 %".68", i32* %".67"
  br label %".39.endif"
.39.endif:
  %".71" = load i32, i32* %"j"
  %".72" = add i32 %".71", 1
  store i32 %".72", i32* %"j"
  br label %".38"
.82:
  %".86" = load i32, i32* %"i"
  %".87" = load i32, i32* %"n"
  %".88" = icmp slt i32 %".86", %".87"
  %".89" = icmp ne i1 %".88", 0
  br i1 %".89", label %".83", label %".84"
.83:
  %".91" = getelementptr inbounds [4 x i8], [4 x i8]* @".str4", i32 0, i32 0
  %".92" = load i32, i32* %"i"
  %".93" = getelementptr inbounds [8 x i32], [8 x i32]* @"a", i32 0, i32 %".92"
  %".94" = load i32, i32* %".93"
  %".95" = call i32 (i8*, ...) @"printf"(i8* %".91", i32 %".94")
  %".96" = load i32, i32* %"i"
  %".97" = add i32 %".96", 1
  store i32 %".97", i32* %"i"
  br label %".82"
.84:
  ret i32 0
}

@".str1" = constant [14 x i8] c"Before sort: \00"
declare i32 @"printf"(i8* %".1", ...) 

@".str2" = constant [4 x i8] c"%d \00"
@".str3" = constant [14 x i8] c"\0aAfter sort: \00"
@".str4" = constant [4 x i8] c"%d \00"
