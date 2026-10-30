// Offscreen regression: a settled splash must not continuously request redraws.
// CPU/frame counts describe the software-rendered test, not live GPU performance.
#include <QGuiApplication>
#include <QQuickView>
#include <QQuickItem>
#include <QTimer>
#include <QElapsedTimer>
#include <QJsonObject>
#include <QJsonDocument>
#include <QTextStream>
#include <sys/resource.h>
int main(int argc,char**argv){
 QGuiApplication app(argc,argv);
 if(argc!=2)return 2;
 QQuickView view; view.setResizeMode(QQuickView::SizeRootObjectToView);view.resize(1280,800);
 int frames=0, ticks=0;
 QObject::connect(&view,&QQuickWindow::frameSwapped,[&](){frames++;});
 QObject::connect(&view,&QQuickWindow::afterAnimating,[&](){ticks++;});
 view.setSource(QUrl::fromLocalFile(QString::fromLocal8Bit(argv[1])));
 if(view.status()!=QQuickView::Ready){for(auto e:view.errors())qCritical()<<e;return 1;}
 view.show();view.rootObject()->setProperty("stage",1);
 rusage before{};QElapsedTimer clock;
 QTimer::singleShot(1400,[&](){frames=0;ticks=0;getrusage(RUSAGE_SELF,&before);clock.start();});
 QTimer::singleShot(4400,[&](){
  rusage after{};getrusage(RUSAGE_SELF,&after);
  auto ms=[](timeval t){return t.tv_sec*1000.0+t.tv_usec/1000.0;};
  QJsonObject out{{"frames",frames},{"animation_ticks",ticks},{"elapsed_ms",double(clock.elapsed())},{"cpu_ms",ms(after.ru_utime)+ms(after.ru_stime)-ms(before.ru_utime)-ms(before.ru_stime)}};
  QTextStream(stdout)<<QJsonDocument(out).toJson(QJsonDocument::Compact)<<"\n";app.exit(frames > 2 ? 1 : 0);
 });
 return app.exec();
}
