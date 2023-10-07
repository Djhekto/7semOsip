#include <iostream>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <bits/stdc++.h>

using namespace std;

#include "include/raylib.h"
#define wWidth 2000
#define wHeight 1000
#define xStart wWidth-1400
#define yStart wHeight-400
#define MASHTAB 200

int main()
{
double y1, y2, x1, x2; // углы
double hx, hy; // шаги
int nomer, bigc; // номер €чейки и счетчик
double a, b; // коэффиценты отображени€
double cx, cy; // бегающий верхний левый угол
double x_l[500], y_l[500]; // список точек рандома и их отображ
int n_us[100]; // список do сортировки и удалени€ лишнего
int big[10000]; //все €чейки после сортировки
int nomer1; //номер €чейки которую мен€ем
int chet;
bigc = 0;
//
puts("--- symv 2 ---");
//
puts("koordinati niznego ugla");
 puts("-1.5 -1.5");
 scanf("%lf", &x1);
 scanf("%lf", &y1);
puts("koordinati verhnego ugla");
 puts("1.5 1.5");
 scanf("%lf", &x2);
 scanf("%lf", &y2);
if (x2<x1) {return 1;}
if (y2<y1) {return 1;}
//
srand (time(NULL));
cx = x1;
cy = y2;
double cto = 20;
hx = ( fabs(x1) + fabs(x2) )/cto;
hy = ( fabs(y1) + fabs(y2) )/cto;
printf("hx = %lf; hy = %lf; \n",hx,hy);
//
puts("a =  ; b =  ");
 puts("0.3  0.2");
 scanf("%lf", &a);
 scanf("%lf", &b);
// оптимизаци€
int nya = (int)((x2-x1)/hx); //клеток в строке
nomer1 = 1;
//kostili
big[bigc] = -1;
bigc++; //костыль
n_us[0] = 0;
n_us[1] = 1;
chet=0;

//
while (cy>y1)
  {
    while (cx<x2)
    {
     for (int i = 0; i < 100; i++) //цикл рандома
        {
            x_l[i] = rand() % (int)(hx*1000);
            x_l[i] = cx + x_l[i]/1000;
            y_l[i] = rand() % (int)(hy*1000);
            y_l[i] = cy - y_l[i]/1000;
       //     printf("%lf  %lf\n",x_l[i],y_l[i]);
        }
     for (int i = 0; i < 100; i++) //цикл отображ
        {
            y_l[i] = 2*x_l[i]*y_l[i] + b;
            x_l[i] = x_l[i]*x_l[i] - y_l[i]*y_l[i] + a;
        }
     for (int i = 0; i < 100; i++) //цикл номеров
        {
       if ( x_l[i]<x1 || x_l[i]>x2 || y_l[i]<y1 || y_l[i]>y2 ) {}
            else{
            nomer =   (((floor(fabs(y2 - y_l[i])/hy) ) * nya)
                          +  floor((fabs(x1 - x_l[i])/hx) + 1) )  ;
          //printf("-%d-",nomer);
            n_us[i] = nomer; chet++;
                }
        }
        sort(n_us, n_us + 100);
        big[bigc] = nomer1;
        bigc++; //запись первого эл
     for (int i = 0; i < chet; i++) //цикл удалени€ и заноса
       {
        if (n_us[i]!=n_us[i+1]) {big[bigc]=n_us[i]; bigc++;}
       }
       chet=0;
      big[bigc] = -1; bigc++; //раздел€ю лист
 nomer1++;cx+=hx;   }
 cy-=hy; cx=x1; }
//
 for (int i = 0; i < bigc; i++) //цикл печати
    {
    if (big[i]==-1) {printf("\n");}
    else {printf("%d ",big[i]);}
    }
//

//
InitWindow(wWidth, wHeight, "zilli-sym");
SetTargetFPS(30);
while (!WindowShouldClose())
    {
BeginDrawing();
ClearBackground(RAYWHITE);
cy = y2;
cx = x1;
bigc=0;
while (cy>y1)
  {
    while (cx<x2)
    {
        while (big[bigc]!=-1)
        {
        bigc++;
        }
        bigc++; bigc++;
        if (big[bigc]!=-1)  {
 DrawRectangle(xStart+cx*MASHTAB,yStart+cy*MASHTAB,(hx*MASHTAB)+1,(hy*MASHTAB)+1,RED);
//  DrawRectangle(xStart+cx*MASHTAB,yStart+cy*MASHTAB,hx*50,hy*50,BLUE);
                            }
cx+=hx;   }
cy-=hy; cx=x1; }
DrawLine(0,yStart,wWidth,yStart,BLACK);
DrawLine(xStart,0,xStart,wHeight,BLACK);
 EndDrawing();
    }


return 0;
}
