; ModuleID = "C Compiler"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"foo"() 
{
entry:
  ret i32 0
}

define i32 @"bar"() 
{
entry:
  ret i32 0
}

define i32 @"main"() 
{
entry:
  %".2" = call i32 @"foo"()
  %".3" = call i32 @"bar"()
  ret i32 0
}

