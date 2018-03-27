#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include <vector>
#include <iostream>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;
using namespace std;
int readFileList(char *basePath, vector<string> &fileNames)
{
    DIR *dir;
    struct dirent *ptr;
    char base[1000];

    if ((dir=opendir(basePath)) == NULL)
    {
        perror("Open dir error...");
        exit(1);
    }

    string path = basePath;

    while ((ptr=readdir(dir)) != NULL)
    {
        if(strcmp(ptr->d_name,".")==0 || strcmp(ptr->d_name,"..")==0)    ///current dire OR parrent dir
            continue;
        else if(ptr->d_type == 8)    ///file
        {
            fileNames.push_back(path + ptr->d_name);
            printf("d_name:%s/%s\n",basePath,ptr->d_name);
        }
        else if(ptr->d_type == 10)    ///link file
            printf("d_name:%s/%s\n",basePath,ptr->d_name);
        else if(ptr->d_type == 4)    ///dir
        {
            memset(base,'\0',sizeof(base));
            strcpy(base,basePath);
            strcat(base,"/");
            strcat(base,ptr->d_name);
            readFileList(base, fileNames);
        }
    }
    closedir(dir);
    return 0;
}

//均值Hash算法
string HashValue(Mat &src)
{
    string rst(64,'\0');
    Mat img;
    if(src.channels()==3)
        cvtColor(src,img,CV_BGR2GRAY);
   else
       img=src.clone();
      /*第一步，缩小尺寸。
        将图片缩小到8x8的尺寸，总共64个像素,去除图片的细节*/

       resize(img,img,Size(8,8));
   /* 第二步，简化色彩(Color Reduce)。
      将缩小后的图片，转为64级灰度。*/

   uchar *pData;
   for(int i=0;i<img.rows;i++)
   {
       pData = img.ptr<uchar>(i);
       for(int j=0;j<img.cols;j++)
       {
           pData[j]=pData[j]/4;            }
   }

       /* 第三步，计算平均值。
      计算所有64个像素的灰度平均值。*/
   int average = mean(img).val[0];

       /* 第四步，比较像素的灰度。
    将每个像素的灰度，与平均值进行比较。大于或等于平均值记为1,小于平均值记为0*/
   Mat mask= (img>=(uchar)average);

       /* 第五步，计算哈希值。*/
   int index = 0;
   for(int i=0;i<mask.rows;i++)
   {
       pData = mask.ptr<uchar>(i);
       for(int j=0;j<mask.cols;j++)
       {
           if(pData[j]==0)
               rst[index++]='0';
           else
               rst[index++]='1';
       }
   }
   return rst;
}

//pHash算法
string pHashValue(Mat &src)
{
    Mat img ,dst;
    string rst(64,'\0');
    double dIdex[64];
    double mean = 0.0;
    int k = 0;
    if(src.channels()==3)
    {
        cvtColor(src,src,CV_BGR2GRAY);
        img = Mat_<double>(src);
    }
    else
    {
        img = Mat_<double>(src);
    }

       /* 第一步，缩放尺寸*/
    resize(img, img, Size(8,8));

       /* 第二步，离散余弦变换，DCT系数求取*/
    dct(img, dst);

       /* 第三步，求取DCT系数均值（左上角8*8区块的DCT系数）*/
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j)
        {
            dIdex[k] = dst.at<double>(i, j);
            mean += dst.at<double>(i, j)/64;
            ++k;
        }
    }

       /* 第四步，计算哈希值。*/
    for (int i =0;i<64;++i)
    {
        if (dIdex[i]>=mean)
        {
            rst[i]='1';
        }
        else
        {
            rst[i]='0';
        }
    }
    return rst;
}

//汉明距离计算
int HanmingDistance(string &str1,string &str2)
{
   if((str1.size()!=64)||(str2.size()!=64))
       return -1;
   int difference = 0;
   for(int i=0;i<64;i++)
   {
       if(str1[i]!=str2[i])
           difference++;
   }
   return difference;
}

int main(int argc, char **argv)
{
    if(argc < 3)
    {
        std::cout << "The argument is less than 3." << std::endl;
        std::cout << "Usage: ./main image_path test_image" << std::endl;
        return 1;
    }
    char *path = argv[1];
    string test_name = argv[2];
    Mat test_img = imread(test_name);
    string test_value = pHashValue(test_img);

    vector<string> file_names;
    readFileList(path, file_names);
    int num_img = file_names.size();
    for(int i = 0; i < num_img; i ++)
    {
        if(file_names[i] == test_name)
        {
            continue;
        }
        Mat tmp_img = imread(file_names[i]);
        string tmp_value = pHashValue(tmp_img);
//        string tmp_value = HashValue(tmp_img);
        int diff = HanmingDistance(test_value, tmp_value);
        cout << i << ", " << file_names[i] << ", diff = " << diff << endl;
    }
    return 0;
}
