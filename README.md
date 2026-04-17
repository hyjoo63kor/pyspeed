# pyspeed

`uv` + Python 3.12 기반으로 Python 속도 향상 아이디어를 실험하는 작은 벤치마크 모음입니다.  
순수 Python 미세 최적화부터 `numpy`, `numba`, `ctypes`, 직접 컴파일한 C DLL, `OpenCV`/`Pillow` 비교까지 한 저장소에서 빠르게 확인할 수 있습니다.

## 포함된 비교

- 순수 Python 루프, 문자열, dict lookup, 캐시, 파일 I/O
- `csv`, `regex`, 문자열 정규화/인코딩
- `threading` vs `multiprocessing`
- `numpy`, `numba`, `numba` warm/cold start
- `ctypes.memmove`와 직접 빌드한 C DLL 호출
- `OpenCV` vs `Pillow`

## 실행 방법

처음 한 번은 가상환경을 준비합니다.

```powershell
.\scripts\setup_env.ps1
```

가상환경을 활성화한 뒤 실행할 수 있습니다.

```powershell
.\.venv\Scripts\Activate.ps1
python -V
python -m pyspeed --list
python -m pyspeed loops
python -m pyspeed loops --timer perf_counter_ns
python -m pyspeed all --profile quick --skip-case parallel
python -m pyspeed all
```

가상환경 활성화 없이 직접 실행해도 됩니다.

```powershell
.\.venv\Scripts\python.exe -m pyspeed strings
```

벤치마크 결과를 파일로 저장하려면:

```powershell
.\scripts\run_benchmarks.ps1
.\scripts\run_benchmarks.ps1 -TimerName perf_counter_ns
.\scripts\run_benchmarks.ps1 -SkipCases parallel
.\\scripts\\run_benchmarks.ps1 -ProfileName full -SkipCases parallel
.\.venv\Scripts\python.exe .\scripts\summarize_results.py results\latest.json
.\.venv\Scripts\python.exe .\scripts\benchmark_numpy_env.py
.\.venv\Scripts\python.exe .\scripts\compare_accelerators.py
```

네이티브 DLL 예제를 빌드하려면:

```powershell
.\scripts\build_native.ps1
.\scripts\build_native.ps1 -Compiler clang
.\.venv\Scripts\python.exe -m pyspeed cdll --profile quick
.\scripts\compare_native_compilers.ps1
```

특정 케이스를 프로파일링하려면:

```powershell
.\scripts\profile_case.ps1 strings
```

타이머 측정 방식을 바꿔 비교하려면:

```powershell
.\.venv\Scripts\python.exe -m pyspeed strings --timer timeit
.\.venv\Scripts\python.exe -m pyspeed strings --timer perf_counter_ns
.\.venv\Scripts\python.exe -m pyspeed csv --profile quick
.\\.venv\\Scripts\\python.exe -m pyspeed opencv_resize --profile quick
.\\.venv\\Scripts\\python.exe -m pyspeed opencv_blur --profile quick
.\.venv\Scripts\python.exe -m pyspeed ctypes --profile quick
.\.venv\Scripts\python.exe -m pyspeed numba_cold --profile quick
```

프로파일 결과 확인:

```powershell
.\.venv\Scripts\python.exe -m pstats results\strings.prof
```

## 코드 위치

핵심 코드는 아래 위치에 있습니다.

- `pyspeed/__main__.py`: `python -m pyspeed` 진입점
- `pyspeed/runner.py`: 케이스 목록, 인자 파싱, 벤치마크 실행
- `pyspeed/cases/`: 성능 비교 예제 모음
- `scripts/setup_env.ps1`: `uv` 기반 Python 3.12 환경 준비
- `scripts/build_native.ps1`: C 소스를 DLL로 컴파일
- `scripts/compare_native_compilers.ps1`: `gcc`와 `clang` DLL 빌드/실행 결과 비교
- `scripts/benchmark_numpy_env.py`: NumPy 버전/BLAS/SIMD 정보와 대표 연산 성능 저장
- `scripts/compare_accelerators.py`: `ctypes` / `cdll` / `numpy` / `numba` 계열 가속 수단 비교 저장
- `scripts/run_benchmarks.ps1`: 전체 벤치마크 실행 후 `results/latest.txt` 저장
- `scripts/profile_case.ps1`: 특정 케이스 `cProfile` 실행
- `scripts/summarize_results.py`: 저장된 JSON 결과를 속도 향상 순으로 요약

예제 코드 파일:

- `pyspeed/cases/loops.py`
- `pyspeed/cases/strings.py`
- `pyspeed/cases/lookups.py`
- `pyspeed/cases/slots_case.py`
- `pyspeed/cases/cache_case.py`
- `pyspeed/cases/dictget_case.py`
- `pyspeed/cases/regex_case.py`
- `pyspeed/cases/csv_case.py`
- `pyspeed/cases/opencv_resize_case.py`
- `pyspeed/cases/opencv_blur_case.py`
- `pyspeed/cases/ctypes_case.py`
- `pyspeed/cases/cdll_case.py`
- `pyspeed/cases/fileio_case.py`
- `pyspeed/cases/normalize_case.py`
- `pyspeed/cases/parallel_cpu_case.py`
- `pyspeed/cases/numpy_case.py`
- `pyspeed/cases/numba_case.py`
- `pyspeed/cases/numba_cold_case.py`

## 현재 상태

- `uv` 실행은 가능
- `uv`가 관리하는 Python 3.12.12 사용 가능
- 가상환경은 `.venv`에 생성됨
- `setup_env.ps1`가 프로젝트 의존성까지 함께 설치
- CLI에서 `timeit` / `perf_counter_ns` 타이머 선택 가능
- CLI에서 `quick` / `full` 측정 프로필 선택 가능
- `scripts/profile_case.ps1`로 `cProfile` 결과 저장 가능
- `scripts/run_benchmarks.ps1`가 텍스트와 JSON 결과를 함께 저장
- `scripts/run_benchmarks.ps1`가 요약 텍스트도 함께 저장
- `scripts/compare_native_compilers.ps1`가 컴파일러 비교 텍스트와 JSON 결과를 저장

## 빠른 가이드

대략적인 선택 기준:

- 문자열 이어붙이기: `strings`처럼 `"".join(...)`이 유리
- 반복 조회/파싱: `regex`, `csv`, `dictget`, `normalize`처럼 루프 밖 전처리가 유리
- 이미지 처리: `opencv_resize`처럼 OpenCV와 Pillow를 같은 입력으로 직접 비교 가능
- 이미지 처리: `opencv_resize`, `opencv_blur`처럼 연산별로 OpenCV/Pillow 우열이 달라질 수 있음
- 외부 C 함수 호출: `ctypes`는 작은 호출을 자주 하는 것보다 큰 블록 작업에 더 적합
- 실제 네이티브 코드 연동: `cdll`처럼 C DLL을 만들어 큰 계산을 넘길 수 있음
- 수치 계산: `numpy`, `numba`가 순수 Python 루프보다 훨씬 유리할 수 있음
- CPU 병렬 처리: `parallel`은 작업량이 충분히 클 때만 `multiprocessing`이 유리
- 일회성 JIT 실행: `numba_cold`처럼 컴파일 비용까지 포함하면 오히려 느릴 수 있음

`quick` 프로필에서 최근 확인한 경향:

| case | tendency |
| --- | --- |
| `strings` | 큰 폭으로 개선되는 편 |
| `regex`, `csv`, `normalize` | 보통 안정적으로 개선되는 편 |
| `opencv_blur` | 같은 이미지 블러에서 OpenCV가 유리한 경우를 보기 좋음 |
| `opencv_resize` | 이미지 리사이즈처럼 OpenCV가 유리한 경우를 보기 좋음 |
| `ctypes` | 큰 메모리 블록 작업에서 개선될 수 있음 |
| `cdll` | 실제 C 코드가 준비되면 큰 계산 블록에서 개선될 수 있음 |
| `dictget`, `fileio`, `numpy` | 중간 정도 개선 |
| `lookups`, `slots`, `loops` | 환경에 따라 차이가 작거나 뒤집힐 수 있음 |
| `numba` | 워밍업 후 반복 실행에서 매우 큰 개선 |
| `numba_cold` | 컴파일 비용 때문에 일회성 실행에서는 불리할 수 있음 |

`quick` 프로필은 빠른 대신 노이즈가 더 큽니다. 결과를 믿고 비교하려면 `full` 프로필이나 JSON 저장 결과를 함께 보는 편이 좋습니다.

## 가속 수단 비교

외부 가속 수단을 고를 때는 대략 이렇게 보면 됩니다:

| tool | strengths | tradeoffs | good fit |
| --- | --- | --- | --- |
| `ctypes` | 기존 C API를 바로 호출하기 쉬움, 큰 블록 작업에 강함 | Python<->C 경계를 자주 넘나들면 손해 보기 쉬움 | 메모리 복사, 버퍼 처리, 이미 있는 C 함수 호출 |
| `cdll` | 직접 만든 C 코드를 호출 가능, 반복 계산을 네이티브로 내리기 좋음 | 빌드 과정과 DLL 관리가 필요함 | 재사용할 계산 커널, 팀 내 공용 네이티브 코드 |
| `numpy` | 설치와 사용이 비교적 쉬움, 배열 연산에 강함 | 벡터화 가능한 형태로 문제를 바꿔야 함 | 대량 수치 배열 연산, 브로드캐스팅, 합계/변환 |
| `numba` | Python 루프를 크게 바꾸지 않고도 매우 빨라질 수 있음 | 첫 호출 JIT 컴파일 비용이 큼 | 반복 실행되는 숫자 루프, warm workload |

현재 `quick` 기준으로 보면:

- `ctypes`: 큰 바이트 블록 복사에서 약 `139x` 수준 개선
- `cdll`: 컴파일한 C DLL 호출 예제에서 약 `47x` 수준 개선
- `numpy`: 벡터화 예제에서 약 `3x` 수준 개선
- `numba`: 워밍업 후 숫자 루프에서 약 `250x` 수준 개선
- `numba_cold`: 컴파일 비용 포함 시 일회성 실행에서는 손해 가능

NumPy는 버전뿐 아니라 wheel 빌드 방식, BLAS/OpenBLAS 연결, SIMD 지원에 따라서도 체감 성능이 달라질 수 있습니다.
이 프로젝트에는 `scripts/benchmark_numpy_env.py`를 넣어 두어서, 버전을 바꾼 뒤 같은 대표 연산을 다시 저장해 비교할 수 있습니다.

실무 감각으로는:

- 벡터화 가능한 배열 문제면 `numpy`를 먼저 검토
- 기존 Python 숫자 루프를 유지하고 싶으면 `numba`를 검토
- 이미 C 코드가 있거나 앞으로 C 코드 자산을 만들 계획이면 `cdll`
- 운영체제/API 수준 함수나 메모리 블록 작업이면 `ctypes`

## 예제 목록

- `loops`: 불필요한 함수 호출과 제곱 연산 대신 단순 산술식과 리스트 컴프리헨션 사용
- `strings`: 반복적인 문자열 `+=` 대신 `"".join(...)` 사용
- `lookups`: 루프 안의 전역/속성 조회를 지역 변수 바인딩으로 줄이기
- `slots`: 일반 dataclass 대신 `slots=True` 사용
- `cache`: 반복 계산에 `functools.lru_cache` 적용
- `dictget`: `try/except KeyError` 대신 `dict.get(...)` 사용
- `regex`: 루프 안에서 패턴 생성 대신 `re.compile(...)` 재사용
- `csv`: `DictReader` 대신 고정 열 인덱스를 쓰는 `csv.reader` 사용
- `opencv_resize`: `cv2.resize`와 `Pillow.resize`를 같은 RGB 이미지로 비교
- `opencv_blur`: `cv2.GaussianBlur`와 `Pillow GaussianBlur`를 같은 RGB 이미지로 비교
- `ctypes`: Python 루프 대신 `ctypes.memmove`로 큰 바이트 블록 복사
- `cdll`: 컴파일한 C DLL을 `ctypes`로 불러서 큰 수치 계산 위임
- `fileio`: 작은 단위 반복 쓰기보다 한 번에 버퍼링해서 쓰기
- `normalize`: 유니코드 정규화와 UTF-8 인코딩을 반복 루프 밖에서 미리 처리
- `parallel`: CPU 바운드 작업에서 `threading` 대신 `multiprocessing` 사용
- `numpy`: Python 루프 대신 NumPy 벡터 연산 사용
- `numba`: 숫자 루프를 Numba JIT로 컴파일해서 반복 실행 가속
- `numba_cold`: Numba 컴파일 비용까지 포함해서 일회성 실행 비용 확인

`parallel` 케이스는 프로세스 생성 비용이 있어서 머신 코어 수와 환경에 따라 차이가 더 크게 나타날 수 있습니다.
샌드박스나 제한된 환경에서는 `parallel` 케이스를 `-SkipCases parallel`로 제외하고 저장하는 편이 안전할 수 있습니다.
`ctypes` 케이스는 C 호출 자체보다 Python에서 원소 단위로 도는 루프를 줄이는 쪽에서 의미가 있습니다.
`cdll` 케이스는 먼저 `.\scripts\build_native.ps1`로 DLL을 만들어야 실행할 수 있고, 현재 스크립트는 `C:\c\bin\gcc.exe`를 우선 사용한 뒤 없으면 PATH의 `gcc`를 사용합니다.
`compare_native_compilers.ps1`를 쓰면 `gcc`와 `clang` 빌드를 같은 `cdll` 케이스로 바로 비교할 수 있습니다.
`numba` 케이스는 첫 호출에서 컴파일 비용이 있으므로, 예제에서는 워밍업 후 반복 실행 성능을 비교합니다.
`numba_cold` 케이스는 컴파일 비용까지 포함하므로 `--profile quick`로 보는 편이 의미가 더 분명합니다.
`numba_cold`는 프로세스 상태와 실행 순서에 따라 편차가 더 클 수 있으므로, 단일 수치보다 경향을 보는 용도로 해석하는 편이 좋습니다.

## 파일 구조

```text
pyspeed/
  __main__.py
  runner.py
  cases/
results/
scripts/
  setup_env.ps1
  run_benchmarks.ps1
  profile_case.ps1
```

## 다음 확장 아이디어
