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
  %".8" = icmp slt i32 %".7", 10
  %".9" = icmp ne i1 %".8", 0
  br i1 %".9", label %".4", label %".5"
.4:
  %".11" = load i32, i32* %"i"
  %".12" = srem i32 %".11", 2
  %".13" = icmp ne i32 %".12", 0
  br i1 %".13", label %".4.if", label %".4.else"
.5:
  ret i32 0
.4.if:
  %".15" = load i32, i32* %"i"
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* %"i"
  br label %".3"
.4.else:
  %".19" = getelementptr inbounds [3 x i8], [3 x i8]* @".str0", i32 0, i32 0
  %".20" = load i32, i32* %"i"
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".19", i32 %".20")
  br label %".4.endif"
.4.endif:
  %".23" = load i32, i32* %"i"
  %".24" = icmp eq i32 %".23", 7
  %".25" = icmp ne i1 %".24", 0
  br i1 %".25", label %".4.endif.if", label %".4.endif.endif"
.4.endif.if:
  br label %".5"
.4.endif.endif:
  %".28" = load i32, i32* %"i"
  %".29" = add i32 %".28", 1
  store i32 %".29", i32* %"i"
  br label %".3"
}

@".str0" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...) 

