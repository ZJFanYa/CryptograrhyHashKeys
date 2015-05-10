%module bigNumDLL
%{
/* Includes the header in the wrapped code */
#include "bigNumDLL.h"
%}

%rename(_in) operator >>;
%rename(_out) operator <<;

/* Parse the header file to generate wrappers */
%include "bigNumDLL.h"