AUTO_RX_VERSION := $(shell PYTHONPATH=../auto_rx python3 -m autorx.version 2>/dev/null || python -m autorx.version)
CFLAGS ?= -O3 -w -Wno-unused-variable -DVER_JSN_STR=\"$(AUTO_RX_VERSION)\"
LDLIBS = -lm

PROGRAMS := rd94rd41drop

all: $(PROGRAMS)

rd94rd41drop: rd94rd41drop.o

rd94rd41drop.o : CFLAGS += -O3

clean:
	$(RM) $(PROGRAMS) $(PROGRAMS:=.o)
