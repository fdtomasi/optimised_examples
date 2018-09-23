#include <Python.h>

static void func(const char * a, const char * b, char * c, char * d) {
    c[0] = 'c';
    c[1] = '\0';
    d[0] = 'd';
    d[1] = '\0';
}

static PyObject * spam_system(PyObject *self, PyObject *args)
{
    const char *s1;
    const char *s2;
    char * s1_new;
    char * s2_new;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2))
        return NULL;
    s1_new = (char *)malloc(sizeof(char)*(sizeof(s1)+sizeof(s2)+1));
    s2_new = (char *)malloc(sizeof(char)*(sizeof(s1)+sizeof(s2)+1));
    s1_new[0] = '\0';
    s2_new[0] = '\0';
    func(s1,s2, s1_new, s2_new);
    return Py_BuildValue("ss", s1_new, s2_new);
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initspam(void)
{
    (void) Py_InitModule("spam", SpamMethods);
}

int
main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initspam();
}
