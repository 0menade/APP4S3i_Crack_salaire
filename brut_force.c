
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <crypt.h>

char* SALT = "$1$nMuYuqAu";
char* vrai_mdp = "$1$nMuYuqAu$6hZ7QC8JVVwjCdc3EFBic1";

int main (int argc, char *argv[]) {

		char test_mdp[4];
		test_mdp[3]='\0';
		int i,j,z;
		for(i=32;i<=126;i++){
			test_mdp[0]=(char)i;

			for(z=32;z<=126;z++){
			test_mdp[1]=(char)z;

				for(j=32;j<=126;j++){

					test_mdp[2]=(char)j;
					char* retour = crypt(test_mdp,SALT);

					if(!strcmp(retour,vrai_mdp)){
	  					printf("mdp: %s\n",test_mdp);
						return 0;
				}
			}
		}
	}

	
	printf("mdp non trouve");
	return -1;
}



