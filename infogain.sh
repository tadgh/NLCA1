#!/bin/sh
java -cp weka.jar weka.attributeSelection.InfoGainAttributeEval -i D:\Github\NLCA1\news.arff -s " weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1"