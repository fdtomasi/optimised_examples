  #include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>

//#define N 10
//typedef int row[N];

int main(int argc, char* argv[]){
  int np, me, n, r;
  int I;
  int i,j;
  int k, M;
  int N = 10;
  float * mat;
  MPI_Status status;

  MPI_Init(&argc,&argv);
  MPI_Comm_size(MPI_COMM_WORLD, &np);
  MPI_Comm_rank(MPI_COMM_WORLD, &me);

// Number of rows assigned to each processor, taking care of the remainder
  n = N / np;
  r = N % np;
  if (np - me <= r) n++; // increase the dimension for the last r processes

  // Allocate local workspace
  mat = (float *) malloc((n+1)*N * sizeof(float));
  // printf("Im process %d and I have to allocate %d cells\n", me, n*N);

  // Column of the first "one" entry
  I = n * me;
  if (np - me <= r) I -= r;

  // Initialise local matrix
  for (i = 0; i < n; i++) {
    for (j = 0; j < N; j++) {
      if(j > I) mat[i*N+j] = me+1;
      else mat[i*N+j] = 0;
    }
    I++;
    //printf("I: %d, mat: %f\n", I, mat[i*N+j]);
  }

  // Print matrix
  if (me == 0) { // i'm the collector
      /* Rank 0: print local buffer */
      for (i = 0; i < n; i++) {
        for (j = 0; j < N; j++) {
          printf("%.1f ", mat[i*N+j]);
        }
        printf("\n");
      }
      /* Receive new data from other processes 
 *      in an ordered fashion and print the buffer */
      for (k = 1; k < np; k++) {
        if(np - k <= r) M = n+1;
        else M = n;
        //printf("From process %d I expect %d cells\n", k, M*N);
        MPI_Recv(mat, M*N, MPI_FLOAT, k, 0, MPI_COMM_WORLD, &status);
        for (i = 0; i < M; i++) {
          for (j = 0; j < N; j++) {
            printf("%.1f ", mat[i*N+j]);
          }
          printf("\n");
        }
      }
  }
  else {
      /* Send local data to Rank 0 */
      MPI_Send(mat, n*N, MPI_FLOAT, 0, 0, MPI_COMM_WORLD);
  }

  free(mat);
  MPI_Finalize();

  return 0;
}

