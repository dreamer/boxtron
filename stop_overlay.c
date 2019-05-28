#define _GNU_SOURCE

#include <dlfcn.h>
#include <string.h>
#include <stdio.h>
 
void *(*orig_dlopen)(const char *filename, int flags);
 
void *dlopen(const char *filename, int flags)
{
	const char *lib = "gameoverlayrenderer.so";
	if (strcmp(lib, filename))
		return orig_dlopen(filename, flags);
	else
		return NULL;
}
 
void _init(void)
{
	printf("Loading hack.\n");
	orig_dlopen = dlsym(RTLD_NEXT, "dlopen");
}
