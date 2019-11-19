#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>


int nodes = 3;
int dim = 2;  //2変数3接点

void gauss_a(double[nodes][nodes],double[nodes]);
void cg(double**,double*,int);
void modified_cholesky(double**,double*,int);
void LD_solver(double**, double*, double*,int);
void FEM(int, char*, int, int);
void init(int, char*);
void boundary(int, int);

int main(int argc,char *argv[]){
  int n = 50;
  int boudary_type;
  for (int i = 0; i < n-4; i++) {
    for (int j = 0; j < n-4; j++) {
      //用いるeleファイル名
      char filename[256];
      char char_i[16];
      char char_j[16];
      sprintf(char_i, "%d", i+1);
      sprintf(char_j, "%d", j+1);
      strcat(filename, "./../triangle/poly/four_holes_");
      strcat(filename, char_i);
      strcat(filename, "_");
      strcat(filename, char_j);
      strcat(filename, ".1.ele");
      //境界条件タイプ
      boudary_type = atoi(argv[1]);
      clock_t start,end;
      double time;
      init(n, filename);
      boundary(n, boudary_type);
      start = clock();
      FEM(n, filename, i+1, j+1);
      free(filename);
      end = clock();
      time = (double)(end-start)/CLOCKS_PER_SEC;
      printf("%d,%lf\n",n,time);
    }
  };
  return 0;
}

// 節点および要素番号を設定する関数
void init(int n, char *filename){
  //節点数
  int N = n*n;
  //要素数 1行目1ブロック目
  int noe = 2*(n-1)*(n-1);
  char *tp;
  FILE *fp;
  char line[256];
  if ((fp = fopen(filename, "r")) == NULL) {
    exit(1);
  }
  if (fgets(line, 256, fp) != NULL) {
    tp = strtok(line, " ");
    noe = atoi(tp);
  }
  int i; //カウンタ
  double coord[N][2];
  int nop[noe][3];


  //座標データを与える(これはOK,後々はファイルから読み取るかも？)
  for(i=0; i<N; i++) {
    coord[i][0] = i % n;
    coord[i][1] = i / n;
  }

  //要素データを与える(.eleファイルから読み取る)
  for (int i = 0; i < noe; i++) {
    if (fgets(line, 256, fp) != NULL) {
      char *ptr;
      ptr = strtok(line, " ");
      int index;
      index = atoi(ptr);
      for (int j = 0; j < 3; j++) {
        ptr = strtok(NULL, " ");
        nop[index-1][j] = (atoi(ptr) - 1);
      }
    }
  }

  fclose(fp);

  //それぞれのデータをファイルに保存
  FILE *file;
  file = fopen("coord.txt","w");
  for(i=0; i<N; i++) {
    fprintf(file,"%lf,%lf\n",coord[i][0],coord[i][1]);
  }
  fclose(file);

  file = fopen("nop.txt","w");
  for(i=0; i<noe; i++) {
    fprintf(file,"%d,%d,%d\n",nop[i][0],nop[i][1],nop[i][2]);
  }
  fclose(file);
}

// 境界条件を与える関数
void boundary(int n, int boundary_type){
  int N = n*n;
  int u[N];
  int i;

  FILE *file;
  file = fopen("boundary.txt","w");

  //基本境界条件を与える

  if (boundary_type == 1) {
    //右辺は0度
    for(i=0; i<N; i++) {
      if(i%n==n-1) {
        u[i] = 0;
        if (i == 1200) {
          u[i] = 100;
        }
        fprintf(file,"%d,%d\n",i,u[i]);
      }
    }
    //右辺真ん中は100度
    u[1200] = 100;
    fprintf(file,"%d,%d\n",1200,u[1200]);
    u[1250] = 100;
    fprintf(file,"%d,%d\n",1250,u[1250]);
    u[1300] = 100;
    fprintf(file,"%d,%d\n",1300,u[1300]);
    u[1150] = 100;
    fprintf(file,"%d,%d\n",1150,u[1150]);
    u[1100] = 100;
    fprintf(file,"%d,%d\n",1100,u[1100]);
  }
  if (boundary_type == 3) {
    //右辺は0度
    for(i=0; i<N; i++) {
      if(i%n==n-1) {
        u[i] = 0;
        if (i == 1200) {
          u[i] = 100;
        }
        fprintf(file,"%d,%d\n",i,u[i]);
      }
    }
    //左辺上下真ん中は100度
    u[2450] = 100;
    fprintf(file,"%d,%d\n",2450,u[2450]);
    u[2400] = 100;
    fprintf(file,"%d,%d\n",2400,u[2400]);
    u[0] = 100;
    fprintf(file,"%d,%d\n",0,u[0]);
    u[50] = 100;
    fprintf(file,"%d,%d\n",50,u[50]);
    u[1200] = 100;
    fprintf(file,"%d,%d\n",1200,u[1200]);
    u[1250] = 100;
    fprintf(file,"%d,%d\n",1250,u[1250]);
    u[1300] = 100;
    fprintf(file,"%d,%d\n",1300,u[1300]);
    u[1150] = 100;
    fprintf(file,"%d,%d\n",1150,u[1150]);
    u[1100] = 100;
    fprintf(file,"%d,%d\n",1100,u[1100]);
  }
  fclose(file);
}


void FEM(int n, char *filename, int x, int y){
  int i,ret,bnum;
  int N = n*n;
  double *u; //各節点の温度
  u = malloc(sizeof(double*)*N);
  for(i=0; i<N; i++) {
    u[i]=0;
  }

  int ele = 2*(n-1)*(n-1); //要素データ数
  char *tp;
  FILE *fp;
  char line[256];
  if ((fp = fopen(filename, "r")) == NULL) {
    exit(1);
  }
  if (fgets(line, 256, fp) != NULL) {
    tp = strtok(line, " ");
    ele = atoi(tp);
  }
  fclose(fp);

  double **coord; //座標データ
  coord = malloc(sizeof(double*)*N);
  for(i=0; i<N; i++) {
    coord[i] = malloc(sizeof(double)*dim);
  }

  int **nop; //要素データ
  nop = malloc(sizeof(int*)*ele);
  for(i=0; i<ele; i++) {
    nop[i] = malloc(sizeof(int)*nodes);
  }

  int blimit = 4*n; //境界条件の要素の上限

  FILE *file;
  file = fopen("coord.txt","r");
  for(i=0; i<N; i++) {
    fscanf( file, "%lf,%lf", &coord[i][0], &coord[i][1]);
  }
  fclose(file);

  file = fopen("nop.txt","r");
  for(i=0; i<ele; i++) {
    fscanf(file,"%d,%d,%d", &nop[i][0], &nop[i][1], &nop[i][2]);
  }
  fclose(file);

  int *b_node_num; //境界条件を持つ節点の番号
  b_node_num = malloc(sizeof(int)*blimit);
  double *tmp; //境界条件をuに渡すためのやつ
  tmp =malloc(sizeof(double)*blimit);

  file = fopen("boundary.txt","r");
  bnum=0;
  while((ret=fscanf(file,"%d,%lf", &b_node_num[bnum], &tmp[bnum])) != EOF) {
    u[b_node_num[bnum]] = tmp[bnum];
    bnum++;
  }
  fclose(file);
  free(tmp);

  //メッシュ面積（全て均等とする）*
  double tmp_s = ((coord[nop[0][0]][0] - coord[nop[0][2]][0]) * (coord[nop[0][1]][1] - coord[nop[0][2]][1]) - (coord[nop[0][1]][0] - coord[nop[0][2]][0]) * (coord[nop[0][0]][1] - coord[nop[0][2]][1]));
  double s = fabs(tmp_s) / 2;
  printf("メッシュ1つあたりの面積は%lfです\n",s); //面積表示

  int j,k,l,buf; //カウンタ
  double a[nodes][nodes],b[nodes],c[nodes][nodes]; //形状関数計算用行列
  double **matrix; //全体剛性マトリックス
  matrix = malloc(sizeof(double*)*N);
  for(i=0; i<N; i++) {
    matrix[i] = malloc(sizeof(double)*N);
    if(matrix[i] == NULL) {
      printf("メモリが確保できません\n");
      exit(1);
    }
  }
  for(i=0; i<N; i++) {
    for(j=0; j<N; j++) {
      matrix[i][j] = 0;
    }
  }

  double part_matrix[nodes][nodes];
  //要素合成マトリックスを作って全体合成マトリックスを計算
  for(i=0; i<ele; i++) {
    //aを定義*
    for(j=0; j<dim; j++) {
      for(k=0; k<nodes; k++) {
        a[k][j] = coord[nop[i][k]][j];
      }
    }
    for(j=0; j<nodes; j++) {
      a[j][nodes-1] = 1;
    }
  

    //形状関数の係数計算*
    /*２次元ならば{(x1,y1,s1),(x2,y2,s2),(x3,y3,s3)}のような配列を作る。
       それぞれｘの係数、ｙの係数、定数項である*/

    for(j=0; j<nodes; j++) {
      for(k=0; k<nodes; k++) {
        b[k]=0;
      }
      b[j]=1;
      gauss_a(a,b);
      for(k=0; k<nodes; k++) {
        c[j][k] = b[k];
      }
    }

    //要素剛性マトリックスの計算*
    for(j=0; j<nodes; j++) {
      for(k=0; k<nodes; k++) {
        for(l=0; l<nodes-1; l++) {
          part_matrix[j][k] += c[j][l] * c[k][l];
        }
        part_matrix[j][k] *= s;
      }
    }

    //全体剛性マトリックスに足しあわせていく*
    for(j=0; j<nodes; j++) {
      for(k=0; k<nodes; k++) {
        matrix[nop[i][j]][nop[i][k]] += part_matrix[j][k];
      }
    }
  }

  //nop開放
  for(i=0; i<ele; i++) {
    free(nop[i]);
  }

  for(i=0; i<bnum; i++) {
    for(j=0; j<N; j++) {
      if(b_node_num[i]==j) {
        matrix[b_node_num[i]][j] = -1;
      }
      else{
        matrix[b_node_num[i]][j] = 0;
      }
    }
  }

  double *u_dash; //各節点の温度
  u_dash = malloc(sizeof(double*)*N);

  for(i=0; i<N; i++) {
    u_dash[i] = 0;
    for(j=0; j<N; j++) {
      u_dash[i] -= matrix[i][j] * u[j];
    }
  }
  //境界条件を全体剛性マトリックスに代入*
  for(i=0; i<bnum; i++) {
    for(j=0; j<N; j++) {
      if(b_node_num[i]==j) {
        matrix[b_node_num[i]][j] = 1;
      }
      else{
        matrix[j][b_node_num[i]] = 0;
      }
    }
  }

  //メモリ解放
  free(b_node_num);

  //uの計算*
  //gauss_u(matrix,u,N);
  cg(matrix,u_dash,N);
  //modified_cholesky(matrix,u_dash,N);

  char *tmp_file_position;
  tmp_file_position = "./tmp_data/four_holes_position_data.csv";
  char *tmp_file_size;
  tmp_file_size = "./tmp_data/four_holes_size_data.csv";
  

  FILE *file_position;
  file_position = fopen(tmp_file_position,"a");
  fprintf(file_position, "%d,", (x/10)*5 + (y/10)+1);
  for(i=0; i<N; i++) {
    if (coord[i][0] == 0) {
      fprintf(file_position, "%lf,", u_dash[i]);
    }
  }
  fprintf(file_position, "\n");
  fclose(file_position);
  FILE *file_size;
  file_size = fopen(tmp_file_size,"a");
  fprintf(file_size, "%d,", 2);
  for(i=0; i<N; i++) {
    if (coord[i][0] == 0) {
      fprintf(file_size, "%lf", u_dash[i]);
    }
  }
  fprintf(file_size, "\n");
  fclose(file_size);

  //メモリ解放
  free(u);
  free(u_dash);
  for(i=0; i<N; i++) {
    free(coord[i]);
  }
}



//形状関数計算に使う用*
void gauss_a(double instead_a[nodes][nodes], double b[nodes]){
  int i, j, k, p;
  double w[nodes];
  double pmax, s;
  double a[nodes][nodes];
  //もらった配列aの中身をかえないようにする
  for(j=0; j<nodes; j++) {
    for(k=0; k<nodes; k++) {
      a[j][k] = instead_a[j][k];
    }
  }

/* 前進消去（ピボット選択）*/
  for(k = 0; k < nodes-1; k++) { /* 第ｋステップ */
    p = k;
    pmax = fabs( a[k][k] );
    for(i = k+1; i < nodes; i++) { /* ピボット選択 */
      if(fabs( a[i][k] ) > pmax) {
        p = i;
        pmax = fabs( a[i][k] );
      }
    }


    if(p != k) { /* 第ｋ行と第ｐ行の交換　*/
      for(i = k; i < nodes; i++) {
        /* 係数行列　*/
        s = a[k][i];
        a[k][i] = a[p][i];
        a[p][i] = s;
      }
      /* 既知ベクトル */
      s = b[k];
      b[k] = b[p];
      b[p] = s;
    }

/* 前進消去 */
    for(i = k +1; i < nodes; i++) { /* 第ｉ行 */
      w[i] = a[i][k] / a[k][k];
      a[i][k] = 0.0;
      /* 第ｋ行を-a[i][k]/a[k][k]倍して、第ｉ行に加える */
      for(j = k + 1; j < nodes; j++) {
        a[i][j] = a[i][j] - a[k][j] * w[i];
      }
      b[i] = b[i] - b[k] * w[i];
    }
  }
/* 後退代入 */
  for(i = nodes - 1; i >= 0; i--) {
    for(j = i + 1; j < nodes; j++) {
      b[i] = b[i] - a[i][j] * b[j];
      a[i][j] = 0.0;
    }
    b[i] = b[i] / a[i][i];
    a[i][i] = 1.0;
  }
}


// CG法
void cg(double **a,double *b,int N){
  double *x,*y,*p,*r;
  x = malloc(sizeof(double*)*N);
  y = malloc(sizeof(double*)*N);
  p = malloc(sizeof(double*)*N);
  r = malloc(sizeof(double*)*N);
  int i,j,k;
  double eps = 1e-8;
  double alfa,rr,py,err,beta;

  for(i = 0; i < N; i++) {
    b[i] *= 1;
    for(j = 0; j < N; j++) {
      a[i][j] *= 1;
    }
  }
  for(i = 0; i < N; i++) {
    x[i] = 0;
  }
  // Axを計算
  for(i = 0; i < N; i++) {
    r[i] = b[i];
    for(j = 0; j < N; j++) {
      r[i] -= a[i][j] * x[j];
    }
    p[i] = r[i];
  }

  for(k = 0; k < N; k++) {
    //ykを求める
    for(i = 0; i < N; i++) {
      y[i] = 0;
      for(j = 0; j < N; j++) {
        y[i] += a[i][j] * p[j];
      }
    }
    //修正係数alfaを計算
    rr = 0.0;
    py = 0.0;
    for(i = 0; i < N; i++) {
      rr += r[i] * r[i];
      py += p[i] * y[i];
    }
    alfa = rr / py;

    //暫定解xと残差ｒの更新,errの計算
    err = 0.0;
    for(i = 0; i < N; i++) {
      x[i] = x[i] + alfa * p[i];
      r[i] = r[i] - alfa * y[i];
      err += r[i] * r[i];
    }

    //収束判定
    if(err < eps * eps) {
      printf("converged\n");
      for(i = 0; i < N; i++) {
        b[i] = x[i];
      }
      return;
    }

    //方向ベクトルｐ修正係数betaの更新
    beta = err / rr;
    for(i =0; i < N; i++) {
      p[i] = r[i] + (beta * p[i]);
    }
  }
  printf("繰り返し終了\n");
  for(i = 0; i < N; i++) {
    b[i] = x[i];
  }
}

void modified_cholesky(double **A, double *b, int N){
  clock_t start,start_solve,end;
  int i,j;
  double **L; //全体剛性マトリックス
  start = clock();
  L = malloc(sizeof(double*)*N);
  for(i=0; i<N; i++) {
    L[i] = malloc(sizeof(double)*N);
    if(L[i] == NULL) {
      printf("メモリが確保できません\n");
      exit(1);
    }
  }

  double d[N];
  L[0][0] = A[0][0];
  d[0] = 1.0/L[0][0];

  for(int i = 1; i < N; ++i) {
    for(int j = 0; j <= i; ++j) {
      double lld = A[i][j];
      for(int k = 0; k < j; ++k) {
        lld -= L[i][k]*L[j][k]*d[k];
      }
      L[i][j] = lld;
    }
    if(L[i][i] == 0) {
      printf("zero");
      //return 0;
    }
    d[i] = 1.0/L[i][i];
  }
  start_solve = clock();
  LD_solver(L,d,b,N);
  end = clock();
  double time_mc = (double)(start_solve-start)/CLOCKS_PER_SEC;
  double time_solve = (double)(end-start_solve)/CLOCKS_PER_SEC;
  for(i=0; i<N; i++) {
    free(L[i]);
  }
  printf("%d,%lf,%lf\n",N,time_mc,time_solve);
}

void LD_solver(double **L, double *D, double *b, int N){
  // 前進代入(forward substitution)
  //  LY=bからYを計算
  for(int i = 0; i < N; i++) {
    double tmp = b[i];
    for(int j = 0; j < i; j++) {
      tmp -= L[i][j]*b[j];
    }
    b[i] = tmp/L[i][i];
  }

  // 後退代入(back substitution)
  //  DLtX=YからXを計算
  for(int i = N-1; i >= 0; --i) {
    double tmp = b[i];
    for(int j = i+1; j < N; ++j) {
      tmp -= D[i]*L[j][i]*b[j];
    }
    b[i] = tmp;
  }
}
