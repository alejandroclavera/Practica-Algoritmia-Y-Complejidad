#include<stdio.h>
#include<stdlib.h>

#define GAP_PENALTY -5

int char_index(char symbol)
{
    if(symbol == 'A')
        return 0;
    else if(symbol == 'G')
        return 1;
    else if(symbol == 'C')
        return 2;
    else if('T')
        return 3;
}

int calc_simil(char sym1, char sym2)
{
    int similarity_matrix[4][4] = {{10,-1,-3,-4},{-1,7,-5,-3},{-3,-5,9,0},{-4,-3,0,8}};    
    if(sym1 != '-' && sym2 !='-' )
        return similarity_matrix[char_index(sym1)][char_index(sym2)];
    return GAP_PENALTY;
}

int max(int num1, int num2)
{
    return (num1 > num2) ? num1 : num2;
}

//Función temporal
void view(int **matrix, int n, int m)
{
    for(int i = 0; i <= n; i++)
    {
        for(int j = 0; j <= m; j++)
        {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }   
}

int calc_needleman_score(char* seq1, int len_seq1, char* seq2, int len_seq2)
{
    int **alig_matrix;
    int score;
    //create and initialize alignament matrix
    alig_matrix = (int**)calloc(len_seq1 + 1 ,sizeof(int*));
    for(int i = 0; i <= len_seq1; i++)
    {
        alig_matrix[i] = (int*)calloc(len_seq2 + 1, sizeof(int));
        alig_matrix[i][0] = GAP_PENALTY * i;
    }

    for(int i = 0; i <= len_seq2; i++)
        alig_matrix[0][i] = GAP_PENALTY * i;

    for(int i = 1; i <= len_seq1; i++)
    {
        for(int j = 1; j <= len_seq2; j++)
        {
            int choice1 = alig_matrix[i-1][j-1] + calc_simil(seq1[i - 1], seq2[j-1]);
            int choice2 = alig_matrix[i-1][j] + GAP_PENALTY;
            int choice3 = alig_matrix[i][j-1] +  GAP_PENALTY;
            alig_matrix[i][j] = max(max(choice1, choice2), choice3);
        }
    }
    score = alig_matrix[len_seq1][len_seq2];
    for(int i = 0; i < len_seq1; i++){
        free(alig_matrix[i]);
        alig_matrix[i] = NULL;
    }
    free(alig_matrix);
    alig_matrix = NULL;
    return score;
}  