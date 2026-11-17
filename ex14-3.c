#pragma warning(disable:4996)
#include <stdio.h>

int main(){
    FILE*file;  //파일 포인터 선언
    char ch1 = 'A', ch2 = 'B';  //파일에 쓸 문자를 자정할 변수 초기화
    
    //oneletter.txt 파일을 쓰기 모드로 열기
    file = fopen("oneletter.txt", "w");
    if (file ==NULL){
        printf("파일을 열수 없습니다.\n");
        return 1;
    }
    //파일에 문자 쓰기
    fputc(ch1, file);
    fputc(ch2, file);

    //파일 닫기
    fclose(file);

    printf("oneletter 파일에 문자 '%c', '%c'를 성공적으로 썼습니다.\n", ch1, ch2);
    return 0;
}
