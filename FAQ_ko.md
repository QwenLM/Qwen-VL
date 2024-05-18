# FAQ

## 설치 및 환경

#### 어떤 버전의 transformers를 사용해야 하나요?

4.31.0 버전을 사용하는 것을 선호합니다.

#### 코드와 체크포인트를 다운로드했는데 모델을 로컬에서 불러올 수 없어요. 어떻게 해야 하나요?

코드를 최신 버전으로 업데이트했는지, 그리고 모든 샤드 체크포인트 파일을 올바르게 다운로드했는지 확인해 주세요.

#### `qwen.tiktoken`을 찾을 수 없어요. 이게 무엇인가요?

이것은 토크나이저의 병합 파일입니다. 이 파일을 다운로드해야 합니다. [git-lfs](https://git-lfs.com) 없이 단순히 깃 저장소를 복제했다면 이 파일을 다운로드할 수 없습니다.

#### transformers_stream_generator/tiktoken/accelerate not found 오류

`pip install -r requirements.txt` 명령을 실행하세요. 이 파일은 [https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt](https://github.com/QwenLM/Qwen-VL/blob/main/requirements.txt)에서 찾을 수 있습니다.
<br><br>


## Demo & Inference

#### 데모가 있나요?

네, 웹 데모는 `web_demo_mm.py`를 참고하세요. 더 많은 정보는 README 파일에서 확인할 수 있습니다.



#### Qwen-VL은 스트리밍을 지원하나요?

아니요. 아직 스트리밍을 지원하지 않습니다.

#### 생성된 내용이 지시사항과 관련 없는 것 같습니다.

Qwen-VL 대신 Qwen-VL-Chat을 로드하고 있는지 확인해 주세요. Qwen-VL은 SFT/Chat 모델과 달리 정렬이 없는 기본 모델이므로 다르게 작동합니다.

#### 양자화를 지원하나요?

아니요. 가능한 빨리 양자화를 지원할 예정입니다.

#### 긴 시퀀스 처리에서 만족스럽지 못한 성능

NTK가 적용되었는지 확인해 주세요. `config.json`의 `use_dynamc_ntk`과 `use_logn_attn`은 `true`로 설정되어야 합니다(`true`가 기본값).
<br><br>


## Tokenizer

#### bos_id/eos_id/pad_id not found 오류

저희 훈련에서는 ``을 구분자 및 패딩 토큰으로만 사용합니다. bos_id, eos_id, pad_id를 tokenizer.eod_id로 설정할 수 있습니다. 토크나이저에 대한 문서에서 토크나이저에 대해 더 알아보세요.