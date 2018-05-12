daisy fleetclassify
====  
Learned graph for classify 2D illustration, [Kancolle(戦艦コレクション 艦これ)]( http://www.dmm.com/netgame/feature/kancolle.html ) / [Azurlane(蒼海航路)]( http://www.azurlane.jp/ ).  
with utility and [twitter bot]( https://twitter.com/DFleetclassify ).  

fleetclassify using NijiFlow[2] and MobileNet[1].  

![twitter bot](document/image/20180512.png)  


# Usage
## Setup
Get this.  
`git clone --depth=1 git@github.com:MichinariNukazawa/daisy_fleetclassify`  

Extract custom [nijiflow][].  
`cd daisy_fleetclassify/`  
`git clone --depth=1 git@github.com:MichinariNukazawa/nijiflow.git`  
`cp nijiflow/nijiflow/classifier.py .`  

## Run on CLI
`python3 fleetclassify.py learned_model/nijinet_v1_1.0_224.graphdef.pb file1 file2...`  


## Run on twitter bot
Botへのメンション(@付きツイート)を付けたQuote Tweet(引用ツイート)をすると、Botが判定結果をReply Tweet(返信)します。  

セットアップは[twitter\_bot\_mock]( https://github.com/MichinariNukazawa/twitter_bot_mock )を参照。  

Run.  
`python3 twitter_bot.py`  



# Training
## Get
[pixivpy\_wrapper][pixivpy_wrapper]にて画像を収集。  
[pixivpy\_wrapper][pixivpy_wrapper]付属スクリプトにてnijiflowデータセット生成スクリプトの読み込み形式に変換。  


## Convert
画像データを、`models/research/slim/create_niji_dataset.py`を用いてデータセット化。  

nijiflowのmodelsを取得する。  
`git clone --depth=1 -b niji https://github.com/fallthrough/models`  

データセット化の実行例:  
```
python3 models/research/slim/create_niji_dataset.py \  
	--output_dir=./drive/fleetclassify_dataset \  
	${HOME}/pixiv_data/image__艦これ/nijiflow_data/nijiflow.list \  
	${HOME}/pixiv_data/image__アズールレーン/nijiflow_data/nijiflow.list  
```

以降の手順は、[References 2][SIG2DLetter1]を参照。(後日公開されるとのことなので)  


# License
Aapache 2.0  


# References
[1] A. G. Howard, M. Zhu, B. Chen, D. Kalenichenko, W. Wang, T. Weyand,  
M. Andreetto, and H. Adam. Mobilenets: Efficient convolutional neural  
networks for mobile vision applications. CoRR, abs/1704.04861, 2017.  

[2] H. Tachibana. [NijiFlow: MobileNets に基づくコンパクトな二次元画像判別機][SIG2DLetter1].  
SIG2D Letters #1, 2017.

[pixivpy_wrapper]: https://github.com/MichinariNukazawa/pixivpy_wrapper  
[SIG2DLetter1]: http://sig2d.org/publications/  

