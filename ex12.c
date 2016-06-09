#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>

int main(int argc, char* argv[]){
  int np, me, r;
  float v;
  unsigned int i, j, k;
  MPI_Status status;

  MPI_Init(&argc,&argv);
  MPI_Comm_size(MPI_COMM_WORLD, &np);
  MPI_Comm_rank(MPI_COMM_WORLD, &me);

  //initialise local matrix
  int * matrix = (int *) malloc(np * np * sizeof(int));
  for(i = 0; i < np; ++i) {
        for(j = 0; j < np; ++j) {
                matrix[i*np+j] = (i==j ? me : 0);
        }
  }
  //print local matrix
  for(i = 0; i < np; ++i) {
        for(j = 0; j < np; ++j) {
                printf("%d ", matrix[i*np+j]);
        }
        printf("\n");
  }

  MPI_Datatype diag;
  // every process allocate their vector from local matrix
  MPI_Type_vector(np, 1, np+1, MPI_INT, &diag);
  MPI_Type_commit(&diag);

  MPI_Gather(matrix, 1, diag, matrix, np, MPI_INT, 0, MPI_COMM_WORLD);
  if(me==0) {
        //print local matrix
        printf("FINAL MATRIX\n");
        for(i = 0; i < np; ++i) {
                for(j = 0; j < np; ++j) {
                        printf("%d ", matrix[i*np+j]);
                }
                printf("\n");
        }
  }

  MPI_Type_free(&diag);
  MPI_Finalize();

  return 0;
                                                             1,19          Top
}
