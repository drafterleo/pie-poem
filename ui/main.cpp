#include "markupform.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MarkupForm w;
    w.show();

    return a.exec();
}
