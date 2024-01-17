<p align="left">
        <a href="README_CN.md">中文</a>&nbsp ｜ &nbsp <a href="README.md">English</a>&nbsp ｜ &nbsp日本語&nbsp
</p>
<br><br>

<p align="center">
    <img src="assets/logo.jpg" width="400"/>
<p>
<br>

<p align="center">
        Qwen-VL <a href="https://modelscope.cn/models/qwen/Qwen-VL/summary">🤖 <a> | <a href="https://huggingface.co/Qwen/Qwen-VL">🤗</a>&nbsp ｜ Qwen-VL-Chat <a href="https://modelscope.cn/models/qwen/Qwen-VL-Chat/summary">🤖 <a>| <a href="https://huggingface.co/Qwen/Qwen-VL-Chat">🤗</a>&nbsp ｜ Qwen-VL-Chat-Int4 <a href="https://huggingface.co/Qwen/Qwen-VL-Chat-Int4">🤗</a>
<br>
<a href="assets/wechat.png">WeChat</a>&nbsp&nbsp | &nbsp&nbsp<a href="https://discord.gg/z3GAxXZ9Ce">Discord</a>&nbsp&nbsp | &nbsp&nbsp<a href="https://modelscope.cn/studios/qwen/Qwen-VL-Chat-Demo/summary">Demo</a>&nbsp ｜ &nbsp<a href="https://arxiv.org/abs/2308.12966">Paper</a>&nbsp&nbsp | &nbsp&nbsp<a href="https://github.com/camenduru/Qwen-VL-Chat-colab">Colab</a>&nbsp&nbsp | &nbsp <a href="TUTORIAL_ja.md">Tutorial</a>
</p>
<br><br>
<p align="left">
        日本語ドキュメントメンテナー: <a href="https://github.com/eltociear">Ikko Eltociear Ashimine</a>
</p>
<br>

**Qwen-VL** （Qwen Large Vision Language Model）は、アリババクラウドが提唱するラージモデルシリーズ Qwen（略称: Tongyi Qianwen）のマルチモーダル版です。Qwen-VL は、画像、テキスト、バウンディングボックスを入力として受け付け、テキストとバウンディングボックスを出力します。Qwen-VL の特徴は以下の通りです:

- **好調なパフォーマンス**: 複数の英語評価ベンチマーク（Zero-shot Captioning、VQA、DocVQA、Grounding を含む）において、同様のモデル規模でオープンソース化された既存の大規模ビジョン言語モデル（LVLM）を大幅に上回ります。
- **テキスト認識をサポートする多言語 LVLM**: Qwen-VL は、英語、中国語、多言語の会話を自然にサポートし、画像内の中国語と英語の二言語テキストのエンドツーエンドの認識を促進します。
- **複数画像のインターリーブ会話**: この機能により、複数の画像を入力し、比較することができる。また、画像に関連する質問を指定し、複数の画像によるストーリーテリングを行うこともできます。
- **中国語のグラウンディングを支える初のジェネラリストモデル**: 中国語と英語のオープンドメイン言語表現によるバウンディングボックスの検出。
- **きめ細やかな認識と理解**: 現在他のオープンソース LVLM で使用されている 224\*224 の解像度と比較して、448\*448 の解像度は、きめ細かいテキスト認識、文書 QA、バウンディングボックス注釈を促進する。

<br>
<p align="center">
    <img src="assets/demo_vl.gif" width="400"/>
<p>
<br>

Qwen-VL シリーズの 2 つのモデルを公開します:

- Qwen-VL: LLM の初期化に Qwen-7B を、視覚エンコーダの初期化に [Openclip ViT-bigG](https://github.com/mlfoundations/open_clip) を用いた学習済み LVLM モデル。そして、それらをランダムに初期化されたクロスアテンションレイヤーで接続する。
- Qwen-VL-Chat: マルチモーダルな LLM ベースの AI アシスタント。Qwen-VL-Chat は、複数の画像入力、複数ラウンドの質問応答、クリエイティブな機能など、より柔軟なインタラクションをサポートします。
  <br>

## ニュースとアップデート
* 2023.11.28 Qwen-VL は、GPT4V、PALI-X を凌駕する最高レベルの [DOCVQA](https://rrc.cvc.uab.es/?ch=17&com=evaluation&task=1) をシングルモデルで達成し、直接画像を入力するだけで様々なタスクを分析理解できる汎用モデルであり。 https://qianwen.aliyun.com のマルチモーダルタブで直接新しいモデルを体験できます。
* 2023.9.25 Qwen-VL-Chat モデルが更新され、中国語コマンドのフォローがより堅牢になり、Web ページと表の画像の理解と質問と回答の機能が向上し、対話のパフォーマンスが向上しました (タッチストーン: 中国語: 401.2->481.7、英語: 645.2->711.6)。
* 2023.9.12 フルパラメータ微調整、LoRA、Q-LoRA を含む、Qwen-VL モデルの微調整をサポートするようになりました。
* 2023.9.8 [Colab](https://github.com/camenduru/Qwen-VL-Chat-c​​olab) のサンプルを提供してくれた [camenduru](https://github.com/camenduru) に感謝します。これをチュートリアルとして使用して、12G GPU でローカルまたはオンラインのデモを行うことができます。
* 2023.9.4 Qwen-VL シリーズは、画像とビデオの両方の理解を含むマルチモーダル LLM を評価するための、正確な人による注釈を備えた 19,000 個の多肢選択質問のマルチモーダル ベンチマークである [Seed-Bench](eval_mm/seed_bench/EVAL_SEED.md) で SOTA を達成します。
* 2023.9.1 基本的な認識と理解だけでなく、文学創作までを含むマルチモーダル言語モデルの包括的な評価である [TouchStone](https://github.com/OFA-Sys/TouchStone) 評価をリリースします 。 強力な LLM を判定者として使用し、マルチモーダルな情報をテキストに変換します。
* 2023.8.31 低メモリコストでありながら推論速度の向上を実現する Qwen-VL-Chat 用の Int4 量子化モデル **Qwen-VL-Chat-Int4** をリリースしました。 また、ベンチマーク評価においても大きなパフォーマンスの低下はありません。
* 2023.8.22 ModelScope と Hugging Face で **Qwen-VL** と **Qwen-VL-Chat** をリリースしました。 また、トレーニングの詳細やモデルのパフォーマンスなど、モデルの詳細については [論文](https://arxiv.org/abs/2308.12966) も提供しています。

## 評価

モデルの能力を2つの観点から評価しました:

1. **標準ベンチマーク**: マルチモーダルなタスクの 4 つの主要カテゴリーについて、モデルの基本的なタスク能力を評価する:
   
   - ゼロショットキャプション: 未見のデータセットに対して、モデルのゼロショット画像キャプション能力を評価する;
   - 一般的な VQA: 判定、色、数、カテゴリなど、画像の一般的な質問応答能力を評価する;
   - テキストベース VQA: 文書 QA、図表 QAなど、写真内のテキストを認識するモデルの能力を評価する;
   - 参照表現理解: 参照表現理解: 参照表現で記述された画像内の対象物を特定する能力を評価する。
2. **TouchStone**: 総合的なテキスト画像対話能力と人間とのアライメントレベルを評価するために、GPT4 によるスコアリングに基づく TouchStone と呼ばれるベンチマークを構築し、LVLM モデルを評価しました。
   
   - TouchStone ベンチマークは、合計 300 以上の画像、800 以上の質問、27 のカテゴリをカバーしています。例えば、属性ベースの Q&A、有名人の認識、詩の作文、複数の画像の要約、商品比較、数学の問題解決などです;
   - 画像の直接入力という GPT4 の現在の制限を打ち破るため、TouchStone は人間のラベル付けによるきめ細かい画像注釈を提供します。これらの詳細な注釈は、質問とモデルの出力と共に、採点のために GPT4 に提示されます。
   - ベンチマークには英語版と中国語版があります。

評価結果は以下の通りです:

Qwen-VL は、複数の VL タスクにおいて、現行の SOTA ジェネラリストモデルを上回り、また、能力範囲の点でより包括的なカバレッジを持ちます。

<p align="center">
    <img src="assets/radar.png" width="600"/>
<p>

### ゼロショットキャプションと一般的な VQA

<table>
<thead>
  <tr>
    <th rowspan="2">Model type</th>
    <th rowspan="2">Model</th>
    <th colspan="2">Zero-shot Captioning</th>
    <th colspan="5">General VQA</th>
  </tr>
  <tr>
    <th>NoCaps</th>
    <th>Flickr30K</th>
    <th>VQAv2<sup>dev</sup></th>
    <th>OK-VQA</th>
    <th>GQA</th>
    <th>SciQA-Img<br>(0-shot)</th>
    <th>VizWiz<br>(0-shot)</th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td rowspan="10">Generalist<br>Models</td>
    <td>Flamingo-9B</td>
    <td>-</td>
    <td>61.5</td>
    <td>51.8</td>
    <td>44.7</td>
    <td>-</td>
    <td>-</td>
    <td>28.8</td>
  </tr>
  <tr>
    <td>Flamingo-80B</td>
    <td>-</td>
    <td>67.2</td>
    <td>56.3</td>
    <td>50.6</td>
    <td>-</td>
    <td>-</td>
    <td>31.6</td>
  </tr>
  <tr>
    <td>Unified-IO-XL</td>
    <td>100.0</td>
    <td>-</td>
    <td>77.9</td>
    <td>54.0</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Kosmos-1</td>
    <td>-</td>
    <td>67.1</td>
    <td>51.0</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>29.2</td>
  </tr>
  <tr>
    <td>Kosmos-2</td>
    <td>-</td>
    <td>80.5</td>
    <td>51.1</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>BLIP-2 (Vicuna-13B)</td>
    <td>103.9</td>
    <td>71.6</td>
    <td>65.0</td>
    <td>45.9</td>
    <td>32.3</td>
    <td>61.0</td>
    <td>19.6</td>
  </tr>
  <tr>
    <td>InstructBLIP (Vicuna-13B)</td>
    <td><strong>121.9</strong></td>
    <td>82.8</td>
    <td>-</td>
    <td>-</td>
    <td>49.5</td>
    <td>63.1</td>
    <td>33.4</td>
  </tr>
  <tr>
    <td>Shikra (Vicuna-13B)</td>
    <td>-</td>
    <td>73.9</td>
    <td>77.36</td>
    <td>47.16</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td><strong>Qwen-VL (Qwen-7B)</strong></td>
    <td>121.4</td>
    <td><b>85.8</b></td>
    <td><b>78.8</b></td>
    <td><b>58.6</b></td>
    <td><b>59.3</b></td>
    <td>67.1</td>
    <td>35.2</td>
  </tr>
  <!-- <tr>
    <td>Qwen-VL (4-shot)</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>63.6</td>
    <td>-</td>
    <td>-</td>
    <td>39.1</td>
  </tr> -->
  <tr>
    <td>Qwen-VL-Chat</td>
    <td>120.2</td>
    <td>81.0</td>
    <td>78.2</td>
    <td>56.6</td>
    <td>57.5</td>
    <td><b>68.2</b></td>
    <td><b>38.9</b></td>
  </tr>
  <!-- <tr>
    <td>Qwen-VL-Chat (4-shot)</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>60.6</td>
    <td>-</td>
    <td>-</td>
    <td>44.45</td>
  </tr> -->
  <tr>
    <td>Previous SOTA<br>(Per Task Fine-tuning)</td>
    <td>-</td>
    <td>127.0<br>(PALI-17B)</td>
    <td>84.5<br>(InstructBLIP<br>-FlanT5-XL)</td>
    <td>86.1<br>(PALI-X<br>-55B)</td>
    <td>66.1<br>(PALI-X<br>-55B)</td>
    <td>72.1<br>(CFR)</td>
    <td>92.53<br>(LLaVa+<br>GPT-4)</td>
    <td>70.9<br>(PALI-X<br>-55B)</td>
  </tr>
</tbody>
</table>

- ゼロショット画像のキャプション付けでは、Qwen-VL は Flickr30K で **SOTA** を達成し、InstructBlip を使用した Nocaps でも競争力のある結果を得ています。
- 一般的な VQA では、Qwen-VL は同じ一般的な LVLM スケール設定で **SOTA** を達成しています。

### テキスト指向VQA（画像中のテキスト理解能力に重点を置く）

<table>
<thead>
  <tr>
    <th>Model type</th>
    <th>Model</th>
    <th>TextVQA</th>
    <th>DocVQA</th>
    <th>ChartQA</th>
    <th>AI2D</th>
    <th>OCR-VQA</th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td rowspan="5">Generalist Models</td>
    <td>BLIP-2 (Vicuna-13B)</td>
    <td>42.4</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>InstructBLIP (Vicuna-13B)</td>
    <td>50.7</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>mPLUG-DocOwl (LLaMA-7B)</td>
    <td>52.6</td>
    <td>62.2</td>
    <td>57.4</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Pix2Struct-Large (1.3B)</td>
    <td>-</td>
    <td><b>76.6</b></td>
    <td>58.6</td>
    <td>42.1</td>
    <td>71.3</td>
  </tr>
  <tr>
    <td>Qwen-VL (Qwen-7B)</td>
    <td><b>63.8</b></td>
    <td>65.1</td>
    <td><b>65.7</b></td>
    <td><b>62.3</b></td>
    <td><b>75.7</b></td>
  </tr>
  <tr>
    <td>Specialist SOTAs<br>(Specialist/Finetuned)</td>
    <td>PALI-X-55B (Single-task FT)<br>(Without OCR Pipeline)</td>
    <td>71.44</td>
    <td>80.0</td>
    <td>70.0</td>
    <td>81.2</td>
    <td>75.0</td>
  </tr>
</tbody>
</table>

- テキスト関連の認識/QA 評価において、Qwen-VL は汎用の LVLM スケール設定で SOTA を達成しています。
- 解像度は上記のいくつかの評価において重要である。解像度が 224 のオープンソースの LVLM モデルの多くは、これらの評価ができないか、画像をカットすることでしか解決できないが、Qwen-VL は解像度を 448 にスケーリングし、エンドツーエンドで評価できるようにしました。Qwen-VL は、一部のタスクにおいて、解像度 1024 の Pix2Struct-Large モデルをも凌駕しています。

### 表現理解の参照

<table>
<thead>
  <tr>
    <th rowspan="2">Model type</th>
    <th rowspan="2">Model</th>
    <th colspan="3">RefCOCO</th>
    <th colspan="3">RefCOCO+</th>
    <th colspan="2">RefCOCOg</th>
    <th>GRIT</th>
  </tr>
  <tr>
    <th>val</th>
    <th>test-A</th>
    <th>test-B</th>
    <th>val</th>
    <th>test-A</th>
    <th>test-B</th>
    <th>val-u</th>
    <th>test-u</th>
    <th>refexp</th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td rowspan="8">Generalist Models</td>
    <td>GPV-2</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>51.50</td>
  </tr>
  <tr>
    <td>OFA-L*</td>
    <td>79.96</td>
    <td>83.67</td>
    <td>76.39</td>
    <td>68.29</td>
    <td>76.00</td>
    <td>61.75</td>
    <td>67.57</td>
    <td>67.58</td>
    <td>61.70</td>
  </tr>
  <tr>
    <td>Unified-IO</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td><b>78.61</b></td>
  </tr>
  <tr>
    <td>VisionLLM-H</td>
    <td></td>
    <td>86.70</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Shikra-7B</td>
    <td>87.01</td>
    <td>90.61</td>
    <td>80.24 </td>
    <td>81.60</td>
    <td>87.36</td>
    <td>72.12</td>
    <td>82.27</td>
    <td>82.19</td>
    <td>69.34</td>
  </tr>
  <tr>
    <td>Shikra-13B</td>
    <td>87.83 </td>
    <td>91.11</td>
    <td>81.81</td>
    <td>82.89</td>
    <td>87.79</td>
    <td>74.41</td>
    <td>82.64</td>
    <td>83.16</td>
    <td>69.03</td>
  </tr>
  <tr>
    <td>Qwen-VL-7B</td>
    <td><b>89.36</b></td>
    <td>92.26</td>
    <td><b>85.34</b></td>
    <td><b>83.12</b></td>
    <td>88.25</td>
    <td><b>77.21</b></td>
    <td>85.58</td>
    <td>85.48</td>
    <td>78.22</td>
  </tr>
  <tr>
    <td>Qwen-VL-7B-Chat</td>
    <td>88.55</td>
    <td><b>92.27</b></td>
    <td>84.51</td>
    <td>82.82</td>
    <td><b>88.59</b></td>
    <td>76.79</td>
    <td><b>85.96</b></td>
    <td><b>86.32</b></td>
    <td>-</td>
  <tr>
    <td rowspan="3">Specialist SOTAs<br>(Specialist/Finetuned)</td>
    <td>G-DINO-L</td>
    <td>90.56&nbsp;&nbsp;</td>
    <td>93.19</td>
    <td>88.24</td>
    <td>82.75</td>
    <td>88.95</td>
    <td>75.92</td>
    <td>86.13</td>
    <td>87.02</td>
    <td>-</td>
  </tr>
  <tr>
    <td>UNINEXT-H</td>
    <td>92.64 </td>
    <td>94.33</td>
    <td>91.46</td>
    <td>85.24</td>
    <td>89.63</td>
    <td>79.79</td>
    <td>88.73</td>
    <td>89.37</td>
    <td>-</td>
  </tr>
  <tr>
    <td>ONE-PEACE</td>
    <td>92.58 </td>
    <td>94.18</td>
    <td>89.26</td>
    <td>88.77</td>
    <td>92.21</td>
    <td>83.23</td>
    <td>89.22</td>
    <td>89.27</td>
    <td>-</td>
  </tr>
</tbody>
</table>

- Qwen-VL は、上記のすべての参照表現理解ベンチマークで **SOTA** を達成した。
- Qwen-VL は中国語の下地データを学習していないが、中国語のキャプションデータと英語の下地データを学習することで、ゼロショットで中国語の下地タスクに汎化することができます。

私たちの実験結果を再現するために、上記の評価スクリプトをすべて提供しています。詳しくは [eval_mm/EVALUATION.md](eval_mm/EVALUATION.md) をお読みください。

### チャット評価

TouchStone は GPT4 によるスコアリングに基づくベンチマークで、テキストと画像の対話および人間とのアライメントレベルにおける LVLM モデルの能力を評価する。合計 300 以上の画像、800 以上の質問、属性ベースの Q&A、有名人の認識、詩の作成、複数の画像の要約、商品比較、数学の問題解決など27のカテゴリをカバーしています。詳しくは [touchstone/README_JA.md](touchstone/README_JA.md) をお読みください。

#### 英語

| Model            | Score |
| ---------------- | ----- |
| PandaGPT         | 488.5 |
| MiniGPT4         | 531.7 |
| InstructBLIP     | 552.4 |
| LLaMA-AdapterV2  | 590.1 |
| LLaVA            | 602.7 |
| mPLUG-Owl        | 605.4 |
| Qwen-VL-Chat     | 645.2 |
| Qwen-VL-Chat-1.1 | 711.6 |

#### 中国語

| Model            | Score |
| ---------------- | ----- |
| VisualGLM        | 247.1 |
| Qwen-VL-Chat     | 401.2 |
| Qwen-VL-Chat-1.1 | 481.7 |

Qwen-VL-Chat は中国語と英語のアライメント評価で最高の結果を得ました。
<br>

### その他のベンチマーク

#### SEED-Bench

SEED-Bench は、マルチモーダル LLM を評価するための正確な人による注釈を備えた 19,000 個の多肢選択式質問のマルチモーダル ベンチマークで、**画像** と **ビデオ** の両方の理解を含む 12 の評価次元をカバーしています。 詳細については、[こちら](eval_mm/seed_bench/EVAL_SEED.md) をご覧ください。

Qwen-VL と Qwen-VL-Chat は、このベンチマークで SOTA を達成しています。

<p align="center">
    <img src="eval_mm/seed_bench/leaderboard.jpg"/>
<p>

## 必要条件

* python 3.8 以上
* pytorch 1.12 以上、2.0 以上を推奨
* CUDA 11.4 以上を推奨（GPU ユーザー向けです）
  <br>

## クイックスタート

以下では、Qwen-VL と Qwen-VL-Chat を 🤖 ModelScope と 🤗 Transformers とともに使う方法を、簡単な例で示します。

コードを実行する前に、環境のセットアップと必要なパッケージのインストールが済んでいることを 確認してください。上記の要件を満たしていることを確認してから、依存するライブラリをインストールしてください。

```bash
pip install -r requirements.txt
```

これで ModelScope や Transformers を使い始めることができます。ビジョンエンコーダについての詳しい使い方は、[チュートリアル](TUTORIAL_ja.md)を参照してください。

#### 🤗 Transformers

Qwen-VL-Chat を推論に使用するために必要なのは、以下に示す数行のコードを入力することだけです。ただし、**最新のコードを使用していることを確認してください。**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
torch.manual_seed(1234)

# Note: デフォルトの動作では、インジェクション攻撃防止機能がオフになりました。
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

# bf16 の使用
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="auto", trust_remote_code=True, bf16=True).eval()
# fp16 の使用
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="auto", trust_remote_code=True, fp16=True).eval()
# cpu のみの使用
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cpu", trust_remote_code=True).eval()
# cuda デバイスの使用
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()

# 生成のためのハイパーパラメータの指定
# model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

# 第 1 回 対話ターン
query = tokenizer.from_list_format([
    {'image': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'}, # ローカルパスまたは url
    {'text': '这是什么?'},
])
response, history = model.chat(tokenizer, query=query, history=None)
print(response)
# 写真はビーチでラブラドールの隣で愛犬と戯れる女性が写っており、彼らは砂の中にいる。

# 第 2 回 対話ターン
response, history = model.chat(tokenizer, '框出图中击掌的位置', history=history)
print(response)
# <ref>击掌</ref><box>(536,509),(588,602)</box>
image = tokenizer.draw_bbox_on_latest_picture(response, history)
if image:
  image.save('1.jpg')
else:
  print("no box")
```

<p align="center">
    <img src="assets/demo_highfive.jpg" width="500"/>
<p>

<details>
  <summary>Running Qwen-VL</summary>

Running Qwen-VL pretrained base model is also simple.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
torch.manual_seed(1234)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL", trust_remote_code=True)

# bf16 の使用
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL", device_map="auto", trust_remote_code=True, bf16=True).eval()
# fp16 の使用
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL", device_map="auto", trust_remote_code=True, fp16=True).eval()
# cpu のみの使用
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL", device_map="cpu", trust_remote_code=True).eval()
# cuda デバイスの使用
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL", device_map="cuda", trust_remote_code=True).eval()

# 生成のためのハイパーパラメータの指定
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL", trust_remote_code=True)

query = tokenizer.from_list_format([
    {'image': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'}, # ローカルパスまたは url
    {'text': 'Generate the caption in English with grounding:'},
])
inputs = tokenizer(query, return_tensors='pt')
inputs = inputs.to(model.device)
pred = model.generate(**inputs)
response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=False)
print(response)
# <img>https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg</img>Generate the caption in English with grounding:<ref> Woman</ref><box>(451,379),(731,806)</box> and<ref> her dog</ref><box>(219,424),(576,896)</box> playing on the beach<|endoftext|>
image = tokenizer.draw_bbox_on_latest_picture(response)
if image:
  image.save('2.jpg')
else:
  print("no box")
```

<p align="center">
    <img src="assets/demo_spotting_caption.jpg" width="500"/>
<p>

</details>

HuggingFaceからモデルのチェックポイントとコードをダウンロードする際にネットワークの問題が発生した場合、ModelScopeからチェックポイントをダウンロードする方法はこちらでございます。

```python
from modelscope import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

# Downloading model checkpoint to a local dir model_dir
# model_dir = snapshot_download('qwen/Qwen-VL')
model_dir = snapshot_download('qwen/Qwen-VL-Chat')


# Loading local checkpoints
# trust_remote_code is still set as True since we still load codes from local dir instead of transformers
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="cuda",
    trust_remote_code=True
).eval()
```

#### 🤖 ModelScope

ModelScope は、MaaS（Model-as-a-Service）のためのオープンソースプラットフォームであり、AI 開発者に柔軟で費用対効果の高いモデルサービスを提供します。同様に、以下のように ModelScope でモデルを実行することができます:

```python
from modelscope import (
    snapshot_download, AutoModelForCausalLM, AutoTokenizer, GenerationConfig
)
import torch
model_id = 'qwen/Qwen-VL-Chat'
revision = 'v1.0.0'

model_dir = snapshot_download(model_id, revision=revision)
torch.manual_seed(1234)

tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
if not hasattr(tokenizer, 'model_dir'):
    tokenizer.model_dir = model_dir
# bf16 の使用
# model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, bf16=True).eval()
# fp16 の使用
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, fp16=True).eval()
# cpu の使用
# model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="cpu", trust_remote_code=True).eval()
# auto の使用
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True).eval()

# 生成のためのハイパーパラメータの指定
model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True)

# 第 1 回 対話ターン
# Either a local path or an url between <img></img> tags.
image_path = 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'
response, history = model.chat(tokenizer, query=f'<img>{image_path}</img>这是什么', history=None)
print(response)
# 写真は、若い女性がビーチで愛犬のラブラドール種と戯れているところ。 二人は浜辺に座り、犬の前脚を上げて触れ合っている。

# 第 2 回 対話ターン
response, history = model.chat(tokenizer, '输出击掌的检测框', history=history)
print(response)
# <ref>"击掌"</ref><box>(211,412),(577,891)</box>
image = tokenizer.draw_bbox_on_latest_picture(response, history)
if image:
  image.save('output_chat.jpg')
else:
  print("no box")
```

<p align="center">
    <img src="assets/demo_highfive.jpg" width="500"/>
<p>
<br>

## 量子化

### 使用方法

私たちは、[AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ)に基づいた新しいソリューションを提供し、Qwen-VL-ChatのためのInt4量子化モデル、Qwen-VL-Chat-Int4[Click here](https://huggingface.co/Qwen/Qwen-VL-Chat-Int4)をリリースします。このモデルは、ほぼ無損失なモデル効果を達成しながら、メモリコストと推論速度の両方のパフォーマンスを向上させます。

ここでは、量子化されたモデルを推論に使用する方法を説明します。始める前に、必要な要件（torch 2.0以上、transformers 4.32.0以上など）を満たしていることを確認し、必要なパッケージをインストールしてください：

```bash
pip install optimum
git clone https://github.com/JustinLin610/AutoGPTQ.git & cd AutoGPTQ
pip install -v .
```

`auto-gptq`のインストールに問題がある場合は、公式の[repo](https://github.com/PanQiWei/AutoGPTQ)をチェックして、ホイールを見つけることをお勧めする。

そうすれば、量子化されたモデルを簡単にロードすることができ、いつもと同じように推論を実行することができる：

```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen-VL-Chat-Int4",
    device_map="auto",
    trust_remote_code=True
).eval()
# Either a local path or an url between <img></img> tags.
image_path = 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'
response, history = model.chat(tokenizer, query=f'<img>{image_path}</img>这是什么', history=None)
print(response)
```

### 性能

ベンチマーク **[TouchStone](https://github.com/OFA-Sys/TouchStone)** において、BF16 モデルと Int4 モデルの両方のモデル性能を例示し、量子化モデルが大きな性能劣化に悩まされないことを見出しました。結果を以下に示します：

| Quantization | ZH         | EN            |
| ------------ | :--------: | :-----------: | 
| BF16         | 401.2      |    645.2      |
| Int4         | 386.6      |    651.4      |

### 推論スピード

BF16 精度と Int4 量子化の下で、画像（258 トークンを要する）のコンテキストで 1792（2048-258）トークンと 7934（8192-258）トークンを生成する平均推論速度（トークン/秒）をそれぞれ測定した。

| Quantization | Speed (2048 tokens) | Speed (8192 tokens) |
| ------------ | :-----------------: | :-----------------: |
| BF16         |        28.87        |        24.32        |
| Int4         |        37.79        |        34.34        |

プロファイリングは、PyTorch 2.0.1 と CUDA 11.4 を搭載したシングル A100-SXM4-80G GPU で実行されます。

### GPU メモリ使用量

また、1792 (2048-258) 個のトークン (画像を含む) をコンテキストとしてエンコードする場合 (および単一のトークンを生成する場合) と、7934 (8192-258) 個のトークン (画像をコンテキストとして生成する場合) をそれぞれ BF16 または Int4 量子化レベルでエンコードする場合の GPU メモリ使用量のピーク値をプロファイリングしました。結果を以下に示します。

| Quantization | Peak Usage for Encoding 2048 Tokens | Peak Usage for Generating 8192 Tokens |
| ------------ | :---------------------------------: | :-----------------------------------: |
| BF16         |               22.60GB               |                28.01GB                |
| Int4         |               11.82GB               |                17.23GB                |

上記のスピードとメモリーのプロファイリングは、[このスクリプト](https://qianwen-res.oss-cn-beijing.aliyuncs.com/profile_mm.py)を使用しています。
<br>

## ファインチューニング

現在、公式のトレーニングスクリプト `finetune.py` を提供しています。さらに、finetune.py のシェルスクリプトを提供し、finetune.py を実行することで、finetune.py を起動することができる。さらに、安心してファインチューニングを開始するためのシェルスクリプトも提供しています。このスクリプトは、[DeepSpeed](https://github.com/microsoft/DeepSpeed) および [FSDP](https://engineering.fb.com/2021/07/15/open-source/fsdp/) を使用したトレーニングをサポートします。弊社が提供するシェル・スクリプトは DeepSpeed を使用するため、事前に DeepSpeed をインストールすることをお勧めします:

学習データを準備するには、すべてのサンプルをリストにまとめ、json ファイルに保存する必要があります。各サンプルは id と会話リストで構成される辞書です。以下は 1 つのサンプルを含む単純なリストの例です:

```json
[
  {
    "id": "identity_0",
    "conversations": [
      {
        "from": "user",
        "value": "你好"
      },
      {
        "from": "assistant",
        "value": "我是Qwen-VL,一个支持视觉输入的大模型。"
      }
    ]
  },
  {
    "id": "identity_1",
    "conversations": [
      {
        "from": "user",
        "value": "Picture 1: <img>https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg</img>\n图中的狗是什么品种？"
      },
      {
        "from": "assistant",
        "value": "图中是一只拉布拉多犬。"
      },
      {
        "from": "user",
        "value": "框出图中的格子衬衫"
      },
      {
        "from": "assistant",
        "value": "<ref>格子衬衫</ref><box>(588,499),(725,789)</box>"
      }
    ]
  },
  { 
    "id": "identity_2",
    "conversations": [
      {
        "from": "user",
        "value": "Picture 1: <img>assets/mm_tutorial/Chongqing.jpeg</img>\nPicture 2: <img>assets/mm_tutorial/Beijing.jpeg</img>\n图中都是哪"
      },
      {
        "from": "assistant",
        "value": "第一张图片是重庆的城市天际线，第二张图片是北京的天际线。"
      }
    ]
  }
]
```

VL タスクの場合、`<img> </img> <ref> </ref> <box> </box>` などの特別なトークンが使用されます。

画像は「画像 ID: `<img>img_path</img>\n{your prompt}`」として表されます。ここで、「id」は会話内の画像の位置を 1 から示します。「img_path」は ローカル ファイル パスまたは Web リンク。

座標ボックスは `<box>(x1,y1),(x2,y2)</box>`・として表されます。ここで、`(x1, y1)` と `(x2, y2)` は範囲内の正規化された値です。 `[0, 1000)`。 対応するテキスト説明は `<ref>text_caption</ref>` によって識別できます。


データ準備の後、提供されているシェルスクリプトを使って微調整を実行することができる。データファイルのパス `$DATA` を忘れずに指定してください。

ファインチューニングのスクリプトを使用することで、以下のことが可能になる：
- フルパラメーター・ファインチューニング
- LoRA
- Q-LoRA

### フルパラメーターファインチューニング
フルパラメータパラメータのファインチューニングを行うには、トレーニングプロセス全体ですべてのパラメータを更新する必要があります。トレーニングを開始するには、以下のスクリプトを実行します：

```bash
# 分散トレーニング。GPU メモリが不足するとトレーニングが破綻するため、シングル GPU のトレーニングスクリプトは提供していません。
sh finetune/finetune_ds.sh
```

シェルスクリプトでは、正しいモデル名またはパス、データパス、出力ディレクトリを指定することを忘れないでください。変更したい場合は、引数 `--deepspeed` を削除するか、要件に基づいて DeepSpeed 設定 json ファイルを変更してください。さらに、このスクリプトは混合精度のトレーニングに対応しており、`--bf16 True` または `--fp16 True` を使用することができます。経験的に、あなたのマシンがbf16をサポートしている場合、私たちのプリトレーニングとアライメントを整合させるためにbf16を使用することをお勧めします。

### LoRA
同様に、LoRA を実行するには、以下のように別のスクリプトを使って実行する。始める前に、`peft` がインストールされていることを確認してください。また、モデル、データ、出力へのパスを指定する必要があります。学習済みモデルには絶対パスを使用することをお勧めします。なぜなら、LoRA はアダプタのみを保存し、アダプタ設定 json ファイルの絶対パスは、ロードする事前学習済みモデルを見つけるために使用されるからです。また、このスクリプトは bf16 と fp16 の両方をサポートしている。

```bash
# シングル GPU トレーニング
sh finetune/finetune_lora_single_gpu.sh
# 分散トレーニング
sh finetune/finetune_lora_ds.sh
```

LoRA ([論文](https://arxiv.org/abs/2106.09685)) は、フルパラメーターによるファインチューニングと比較して、adapter のパラメーターを更新するだけで、元の大きな言語モデル層は凍結されたままである。そのため、メモリコストが大幅に削減でき、計算コストも削減できる。

なお、チャットモデル（Qwen-VL-Chatなど）ではなく、ベース言語モデル（Qwen-VLなど）の微調整にLoRAを使用した場合、スクリプトは自動的に学習可能なパラメータとして埋め込み層と出力層を切り替えます。これは、ベースとなる言語モデルには、ChatMLフォーマットによってもたらされる特殊なトークンに関する知識がないためです。したがって、これらのレイヤーは、モデルがトークンを理解し予測するために更新される必要があります。別の言い方をすれば、もしLoRAで特殊なトークンを学習するのであれば、コード内で `modules_to_save` を設定することで、レイヤーを学習可能なパラメータに設定する必要があります。さらに、LoRAのメモリフットプリントは、このような学習可能なパラメータがある場合とない場合で、大きな開きがあることがわかります。そのため、メモリに問題がある場合は、LoRAのChatモデルを微調整することをお勧めします。詳細は以下のプロファイルを参照してください。

### Q-LoRA
しかし、それでもメモリ不足に悩む場合は、Q-LoRA（[論文](https://arxiv.org/abs/2305.14314)）を検討することができます。これは、量子化されたラージ言語モデルと、ページド・アテンションなどの他のテクニックを使用し、さらに少ないメモリコストで実行することができます。Q-LoRA を実行するには、以下のスクリプトを直接実行してください：


```bash
# シングルGPUトレーニング
sh finetune/finetune_qlora_single_gpu.sh
# 分散トレーニング
sh finetune/finetune_qlora_ds.sh
```

Q-LoRA については、弊社が提供する量子化モデル、例えば Qwen-7B-Chat-Int4 をロードすることをお勧めします。ただし、フルパラメータ・ファインチューニングや LoRA とは異なり、Q-LoRA では fp16 のみがサポートされる。

LoRA と Q-LoRA の学習は、フルパラメータによるファインチューニングとは異なり、アダプターパラメータのみを保存する。仮に Qwen-7B から学習を開始したとすると、以下のようにファインチューニングされたモデルを読み込んで推論を行うことができる：

```python
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(
    path_to_adapter, # path to the output directory
    device_map="auto",
    trust_remote_code=True
).eval()
```
アダプターをマージし、微調整したモデルをスタンドアロンモデルとして保存したい場合は（これは LoRA でのみ可能で、Q-LoRA からパラメータをマージすることはできません）、以下のコードを実行します：

```python
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(
    path_to_adapter, # path to the output directory
    device_map="auto",
    trust_remote_code=True
).eval()

merged_model = model.merge_and_unload()
# max_shard_size and safe serialization are not necessary. 
# They respectively work for sharding checkpoint and save the model to safetensors
merged_model.save_pretrained(new_model_directory, max_shard_size="2048MB", safe_serialization=True)
```

注意：マルチGPUトレーニングの場合、分散トレーニング用の適切なハイパーパラメータをマシンに応じて指定する必要があります。また、データ、メモリフットプリント、トレーニング速度を考慮して、引数 `--model_max_length` で最大シーケンス長を指定することをお勧めします。


### メモリと速度のプロファイリング
シングルGPUトレーニングのセットアップにおいて、LoRA (LoRA (Base)はembeddingと出力層を学習させるが、LoRA (Chat)はembeddingと出力層を学習させない) とQ-LoRAのGPUメモリとトレーニング速度をプロファイリングする。このテストでは、シングルA100-SXM4-80G GPUで実験し、CUDA 11.8とPytorch 2.0を使用します。各サンプルには写真が含まれています。384、512、1024、2048という異なる長さの入力のメモリ（GB）と速度（s/iter）をプロファイリングします。統計量を以下に示す：
<table>
    <tr>
 <th rowspan="2">Method</th><th colspan="4" align="center">Sequence Length</th>
    </tr>
    <tr>
        <th align="center">384</th><th align="center">512</th><th align="center">1024</th><th align="center">2048</th>
    </tr>
    <tr>
      <td>LoRA (Base)</td><td align="center">37.1G / 2.3s/it</td><td align="center">37.3G / 2.4s/it</td><td align="center">38.7G / 3.6s/it</td><td align="center">38.7G / 6.1s/it</td>
    </tr>
    <tr>
      <td>LoRA (Chat)</td><td align="center">23.3G / 2.2s/it</td><td align="center">23.6G / 2.3s/it</td><td align="center">25.1G / 3.5s/it</td><td align="center">27.3G / 5.9s/it</td>
    </tr>
    <tr>
        <td>Q-LoRA</td><td align="center">17.0G / 4.2s/it</td><td align="center">17.2G / 4.5s/it</td><td align="center">18.2G / 5.5s/it</td><td align="center">19.3G / 7.9s/it</td>
    </tr>

</table>

シェルスクリプトは `torchrun` を使用してシングル GPU またはマルチGPUトレーニングを実行します。そのため、分散トレーニングのための適切なハイパーパラメータをマシンに応じて指定する必要があります。
<br><br>

## デモ

### Web UI

Web UI デモを構築するためのコードを提供します。始める前に、以下のパッケージがインストールされていることを確認してください:

```bash
pip install -r requirements_web_demo.txt
```

次に以下のコマンドを実行し、生成されたリンクをクリックします:

```bash
python web_demo_mm.py
```

<br>

## FAQ

問題が発生した場合は、[FAQ](FAQ_ja.md) や issue を参照し、新しい issue を立ち上げる前に解決策を探してください。
<br>

## ライセンス契約

研究者や開発者は、Qwen-VL と Qwen-VL-Chat のコードとモデルウェイトを自由に使用することができます。また、商用利用も可能です。詳しくは [LICENSE](LICENSE) をご覧ください。
<br>

## 引用

私たちの論文やコードがあなたの研究に役立つとお感じになりましたら、スター :star: と 引用 :pencil: をお付けください :)

```BibTeX
@article{Qwen-VL,
  title={Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond},
  author={Bai, Jinze and Bai, Shuai and Yang, Shusheng and Wang, Shijie and Tan, Sinan and Wang, Peng and Lin, Junyang and Zhou, Chang and Zhou, Jingren},
  journal={arXiv preprint arXiv:2308.12966},
  year={2023}
}
```
<br>

## お問い合わせ

研究チームまたは製品チームへのメッセージは、qianwen_opensource@alibabacloud.com までお気軽にお送りください。

