# CVPR 2026 Trends — Free-form Analysis

_generated: 2026-05-19 10:04 JST · embedding: `text-embedding-3-small` · labeling+narrative: `gpt-5-mini` · papers: 1650 (is_cvpr2026=yes)_

> このレポートは 31種固定タスクタクソノミ (task_primary / task_secondary / modality) を **使わず**、自由記述の `task_keywords` と embedding を素材に生成しています。

## 1. ベース統計

- **N = 1650** papers (is_cvpr2026=yes)
- with repo URL: **116** (7.0%)
- track 内訳: main=1283, workshop=198, findings=167, other=2

## 2. 自由記述キーワード Top 50 (頻度集計のみ)

| rank | keyword | count |
|---:|---|---:|
| 1 | `diffusion models` | 76 |
| 2 | `reinforcement learning` | 67 |
| 3 | `multimodal` | 57 |
| 4 | `3d gaussian splatting` | 45 |
| 5 | `multimodal large language models` | 41 |
| 6 | `text-to-image` | 41 |
| 7 | `clip` | 39 |
| 8 | `benchmark` | 38 |
| 9 | `vision-language models` | 38 |
| 10 | `semantic segmentation` | 28 |
| 11 | `self-supervised` | 28 |
| 12 | `temporal consistency` | 24 |
| 13 | `generative models` | 21 |
| 14 | `multimodal reasoning` | 20 |
| 15 | `open-vocabulary` | 20 |
| 16 | `transformer` | 19 |
| 17 | `diffusion model` | 19 |
| 18 | `contrastive learning` | 18 |
| 19 | `video understanding` | 17 |
| 20 | `spatial reasoning` | 17 |
| 21 | `synthetic data` | 17 |
| 22 | `visual grounding` | 17 |
| 23 | `dataset` | 17 |
| 24 | `multimodal models` | 17 |
| 25 | `test-time adaptation` | 16 |
| 26 | `large language models` | 16 |
| 27 | `remote sensing` | 15 |
| 28 | `few-shot learning` | 15 |
| 29 | `zero-shot` | 15 |
| 30 | `vision transformers` | 15 |
| 31 | `anomaly detection` | 15 |
| 32 | `3d object detection` | 14 |
| 33 | `self-supervised learning` | 14 |
| 34 | `image restoration` | 14 |
| 35 | `robustness` | 14 |
| 36 | `gaussian splatting` | 14 |
| 37 | `point cloud` | 14 |
| 38 | `visual question answering` | 13 |
| 39 | `multi-modal` | 13 |
| 40 | `temporal coherence` | 13 |
| 41 | `semantic alignment` | 12 |
| 42 | `chain-of-thought` | 12 |
| 43 | `motion generation` | 12 |
| 44 | `cross-attention` | 12 |
| 45 | `domain adaptation` | 12 |
| 46 | `visual reasoning` | 11 |
| 47 | `vision-language model` | 11 |
| 48 | `domain generalization` | 11 |
| 49 | `dynamic scenes` | 11 |
| 50 | `image editing` | 11 |

## 3. 出現クラスタ (35 clusters, size desc)

embedding (= title + task_keywords + abstract head) を `text-embedding-3-small` で取り、KMeans(35) でクラスタリング後、各クラスタの centroid 近傍と頻出キーワードを `gpt-5-mini` にラベル付けさせています。

### Multi-View 3D Perception and Reconstruction  _(N=96)_

このクラスターは multi-view カメラや LiDAR 由来の point clouds を統合し、depth estimation、3D reconstruction、3D object detection といったタスクを視点頑健かつオンラインで扱う研究群です。特徴は transformer や self-supervised 学習、3D foundation models を活用して global consistency のある再構築や cross-modal alignment、occupancy 推定を実現し、自動運転や3Dトラッキングへの応用を目指している点です。

- **top keywords**: `3d object detection`×9, `transformer`×4, `point clouds`×4, `self-supervised`×4, `depth estimation`×3, `lidar`×3, `multi-view`×3, `structure-from-motion`×3
- **representative**:
  - [Unlocking the Power of Critical Factors for 3D Visual Geometry Estimation](http://arxiv.org/abs/2604.21713v1)
  - [Towards Viewpoint-Robust End-to-End Autonomous Driving with 3D Foundation Model Priors](http://arxiv.org/abs/2604.00597v1)
  - [FF3R: Feedforward Feature 3D Reconstruction from Unconstrained views](http://arxiv.org/abs/2604.09862v1)
  - [Dr.Occ: Depth- and Region-Guided 3D Occupancy from Surround-View Cameras for Autonomous Driving](http://arxiv.org/abs/2603.01007v3)
  - [TALO: Pushing 3D Vision Foundation Models Towards Globally Consistent Online Reconstruction](http://arxiv.org/abs/2512.02341v3)
  - [CoIn3D: Revisiting Configuration-Invariant Multi-Camera 3D Object Detection](http://arxiv.org/abs/2603.05042v2)
  - [PE3R: Perception-Efficient 3D Reconstruction](http://arxiv.org/abs/2503.07507v2)
  - [LAMP: Localization Aware Multi-camera People Tracking in Metric 3D World](http://arxiv.org/abs/2605.05390v1)

### Multimodal Video Temporal Grounding and Segmentation  _(N=84)_

このクラスタは multimodal large language models を用いて、temporal grounding や temporal localization、referring video object segmentation といった細粒度の spatio-temporal video understanding を長時間動画に対して統合的に扱う研究群です。特に temporal consistency、visual token sampling、query augmentation と memory/compression を組み合わせて pixel-level 精度と長期依存の推論を両立させる点がユニークです。

- **top keywords**: `video understanding`×6, `video temporal grounding`×6, `temporal consistency`×6, `self-supervised learning`×5, `multimodal large language models`×4, `temporal localization`×4, `video object segmentation`×3, `referring video object segmentation`×3
- **representative**:
  - [Mamba-VMR: Multimodal Query Augmentation via Generated Videos for Precise Temporal Grounding](http://arxiv.org/abs/2603.22121v1)
  - [Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing](http://arxiv.org/abs/2603.12254v1)
  - [Scene-VLM: Multimodal Video Scene Segmentation via Vision-Language Models](http://arxiv.org/abs/2512.21778v2)
  - [UFVideo: Towards Unified Fine-Grained Video Cooperative Understanding with Large Language Models](http://arxiv.org/abs/2512.11336v2)
  - [VSI: Visual Subtitle Integration for Keyframe Selection to enhance Long Video Understanding](http://arxiv.org/abs/2508.06869v4)
  - [VIRST: Video-Instructed Reasoning Assistant for SpatioTemporal Segmentation](http://arxiv.org/abs/2603.27060v1)
  - [SPARROW: Learning Spatial Precision and Temporal Referential Consistency in Pixel-Grounded Video MLLMs](http://arxiv.org/abs/2603.12382v1)
  - [Video Panels for Long Video Understanding](http://arxiv.org/abs/2509.23724v2)

### Open-Vocabulary Self-Supervised 3D Segmentation  _(N=79)_

このクラスタは open-vocabulary や self-supervised 手法を中心に、3D semantic segmentation／instance／panoptic segmentation をリモートセンシング、LiDAR、自動運転、医療など異なるドメインで一般化・ゼロショット化する研究群です。domain adaptation、out-of-distribution 検出、masked representation modeling や reconstructive foundation priors、hierarchical geometric guidance といった技術でラベル不足やドメイン差を克服する点が特徴です。

- **top keywords**: `semantic segmentation`×18, `self-supervised`×6, `open-vocabulary`×5, `remote sensing`×5, `dinov3`×4, `instance segmentation`×3, `semi-supervised learning`×3, `semantic alignment`×3
- **representative**:
  - [GeoGuide: Hierarchical Geometric Guidance for Open-Vocabulary 3D Semantic Segmentation](http://arxiv.org/abs/2603.26260v1)
  - [MoonSeg3R: Monocular Online Zero-Shot Segment Anything in 3D with Reconstructive Foundation Priors](http://arxiv.org/abs/2512.15577v2)
  - [EvObj: Learning Evolving Object-centric Representations for 3D Instance Segmentation without Scene Supervision](http://arxiv.org/abs/2605.13152v1)
  - [Learning Generalizable 3D Medical Image Representations from Mask-Guided Self-Supervision](http://arxiv.org/abs/2603.13660v1)
  - [Masked Representation Modeling for Domain-Adaptive Segmentation](http://arxiv.org/abs/2509.13801v2)
  - [UniGeoSeg: Towards Unified Open-World Segmentation for Geospatial Scenes](http://arxiv.org/abs/2511.23332v3)
  - [Learning to Identify Out-of-Distribution Objects for 3D LiDAR Anomaly Segmentation](http://arxiv.org/abs/2604.23604v1)
  - [PanDA: Unsupervised Domain Adaptation for Multimodal 3D Panoptic Segmentation in Autonomous Driving](http://arxiv.org/abs/2604.19379v1)

### Open-Vocabulary Few-Shot Anomaly Detection  _(N=75)_

このクラスタは anomaly detection と object detection を few-shot / zero-shot や open-vocabulary 設定で扱い、vision-language models や multimodal prototypes を活用してラベル不足や novel category 発見を解決する研究群です。ユニークなのは training-free や parameter-efficient な手法、pseudo-label evolution や subspace modeling といった、少ない注釈で汎化や novel class 検出を可能にする具体的戦略に焦点を当てている点です。

- **top keywords**: `anomaly detection`×10, `few-shot learning`×5, `open-vocabulary`×4, `zero-shot`×4, `object detection`×4, `multimodal`×4, `vision-language models`×3, `active learning`×3
- **representative**:
  - [Hard to See, Hard to Label: Generative and Symbolic Acquisition for Subtle Visual Phenomena](http://arxiv.org/abs/2604.22990v2)
  - [SubspaceAD: Training-Free Few-Shot Anomaly Detection via Subspace Modeling](http://arxiv.org/abs/2602.23013v3)
  - [Learning Multi-Modal Prototypes for Cross-Domain Few-Shot Object Detection](http://arxiv.org/abs/2602.18811v1)
  - [NoOVD: Novel Category Discovery and Embedding for Open-Vocabulary Object Detection](http://arxiv.org/abs/2603.21069v1)
  - [MonoSAOD: Monocular 3D Object Detection with Sparsely Annotated Label](http://arxiv.org/abs/2604.01646v2)
  - [Parameter-Efficient Semantic Augmentation for Enhancing Open-Vocabulary Object Detection](http://arxiv.org/abs/2604.04444v1)
  - [AnomalyVFM -- Transforming Vision Foundation Models into Zero-Shot Anomaly Detectors](http://arxiv.org/abs/2601.20524v2)
  - [EReCu: Pseudo-label Evolution Fusion and Refinement with Multi-Cue Learning for Unsupervised Camouflage Detection](http://arxiv.org/abs/2603.11521v1)

### Multimodal Imaging and Neural Reconstruction  _(N=72)_

このクラスターはneural radiance fieldsやneural fieldsを軸に、low-light、multispectral、infrared-visible fusion、LiDARやeventセンサといったマルチモーダル入力からのjoint reconstruction、relighting、denoisingやimage restorationを扱う点が特徴です。センサ物理を組み込んだ復元やpose-free view synthesis、training-free diffusion harmonizationなど、物理モデルと学習ベース手法を融合して暗所・ノイズ・スペクトル差といった過酷条件下で頑健な出力を得る研究が多く含まれます。

- **top keywords**: `neural radiance fields`×4, `image restoration`×4, `remote sensing`×3, `infrared-visible fusion`×3, `denoising`×3, `relighting`×2, `composed image retrieval`×2, `noisy triplet correspondence`×2
- **representative**:
  - [GeoRelight: Learning Joint Geometrical Relighting and Reconstruction with Flexible Multi-Modal Diffusion Transformers](http://arxiv.org/abs/2604.20715v1)
  - [Seeing through Light and Darkness: Sensor-Physics Grounded Deblurring HDR NeRF from Single-Exposure Images and Events](http://arxiv.org/abs/2601.15475v4)
  - [Perspective-Equivariant Fine-tuning for Multispectral Demosaicing without Ground Truth](http://arxiv.org/abs/2603.01332v2)
  - [Multinex: Lightweight Low-light Image Enhancement via Multi-prior Retinex](http://arxiv.org/abs/2604.10359v2)
  - [Differentiable Adaptive 4D Structured Illumination for Joint Capture of Shape and Reflectance](http://arxiv.org/abs/2605.06214v1)
  - [Customized Fusion: A Closed-Loop Dynamic Network for Adaptive Multi-Task-Aware Infrared-Visible Image Fusion](http://arxiv.org/abs/2604.08924v1)
  - [Spectral-Geometric Neural Fields for Pose-Free LiDAR View Synthesis](http://arxiv.org/abs/2603.12903v1)
  - [HarmoniDiff-RS: Training-Free Diffusion Harmonization for Satellite Image Composition](http://arxiv.org/abs/2604.19392v1)

### Robust Multimodal Large Language Models  _(N=66)_

このクラスタは multimodal large language models の視覚的頑健性と文脈依存性の改善に焦点を当てており、visual representation degradation や contextual blindness、fine-grained visual discrepancy への対処を通じて実世界の視覚推論性能を高める点が特徴です。Context-aware fine-tuning、ReCALL のような再校正手法、event streaming、mixture-of-experts や reinforcement learning を用いたアプローチで能力劣化や注意挙動の解析・補正を行う研究が集まっています。

- **top keywords**: `multimodal large language models`×19, `multimodal`×10, `reinforcement learning`×8, `multimodal reasoning`×4, `large language models`×4, `multimodal models`×4, `mixture-of-experts`×3, `in-context learning`×3
- **representative**:
  - [Predictive Regularization Against Visual Representation Degradation in Multimodal Large Language Models](http://arxiv.org/abs/2603.20808v1)
  - [Visual Funnel: Resolving Contextual Blindness in Multimodal Large Language Models](http://arxiv.org/abs/2512.10362v2)
  - [DUALVISION: RGB-Infrared Multimodal Large Language Models for Robust Visual Reasoning](http://arxiv.org/abs/2604.18829v1)
  - [CoVFT: Context-aware Visual Fine-tuning for Multimodal Large Language Models](http://arxiv.org/abs/2603.21077v2)
  - [Mario: Multimodal Graph Reasoning with Large Language Models](http://arxiv.org/abs/2603.05181v2)
  - [ReCALL: Recalibrating Capability Degradation for MLLM-based Composed Image Retrieval](http://arxiv.org/abs/2602.01639v2)
  - [Learning to See through Illumination Extremes with Event Streaming in Multimodal Large Language Models](http://arxiv.org/abs/2603.27558v1)
  - [Large Multimodal Models as General In-Context Classifiers](http://arxiv.org/abs/2602.23229v1)

### Efficient Diffusion Model Acceleration and Tuning  _(N=62)_

このクラスタは diffusion models の推論・学習・微調整を高速化・省メモリ化する手法群に集中しており、feature caching、diffusion transformers 向けの dynamic patch sampling や block skipping、データ駆動の linear predictor などの工夫を組み合わせている。対象タスクは image generation や image restoration、super-resolution といった高品質な画像合成・復元を低計算コストで実現する点にある。

- **top keywords**: `diffusion models`×30, `diffusion model`×7, `feature caching`×5, `diffusion transformers`×4, `super-resolution`×4, `denoising`×3, `imagenet`×3, `latent diffusion models`×3
- **representative**:
  - [DiP: Taming Diffusion Models in Pixel Space](http://arxiv.org/abs/2511.18822v3)
  - [NanoSD: Edge Efficient Foundation Model for Real Time Image Restoration](http://arxiv.org/abs/2601.09823v2)
  - [LESA: Learnable Stage-Aware Predictors for Diffusion Model Acceleration](http://arxiv.org/abs/2602.20497v2)
  - [Accelerating Diffusion Model Training under Minimal Budgets: A Condensation-Based Perspective](http://arxiv.org/abs/2507.05914v3)
  - [Memory-Efficient Fine-Tuning Diffusion Transformers via Dynamic Patch Sampling and Block Skipping](http://arxiv.org/abs/2603.20755v1)
  - [PixelDiT: Pixel Diffusion Transformers for Image Generation](http://arxiv.org/abs/2511.20645v2)
  - [Beyond Fixed Formulas: Data-Driven Linear Predictor for Efficient Diffusion Models](http://arxiv.org/abs/2604.26365v1)
  - [DMin: Scalable Training Data Influence Estimation for Diffusion Models](http://arxiv.org/abs/2412.08637v4)

### Human-Object Interaction 4D Motion Reconstruction  _(N=61)_

このクラスターは、人間と物体の複雑な相互作用を含む全身および手の動作を、monocularやegocentric映像、マルチモーダルセンサから3D/4Dで生成・再構築する研究群です。motion generationやmotion reconstruction、sim-to-realやmodular controllerの活用、markerlessデータセット構築を通じて、ARやrobot learning向けの現実的なHOI合成・キャプチャを目指している点が特徴です。

- **top keywords**: `motion generation`×5, `human-object interaction`×5, `3d human pose`×3, `egocentric video`×3, `motion reconstruction`×2, `augmented reality`×2, `robot learning`×2, `egocentric`×2
- **representative**:
  - [PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation](http://arxiv.org/abs/2603.22193v3)
  - [ArtHOI: Taming Foundation Models for Monocular 4D Reconstruction of Hand-Articulated-Object Interactions](http://arxiv.org/abs/2603.25791v1)
  - [AnyLift: Scaling Motion Reconstruction from Internet Videos via 2D Diffusion](http://arxiv.org/abs/2604.17818v1)
  - [Dynamic Full-body Motion Agent with Object Interaction via Blending Pre-trained Modular Controllers](http://arxiv.org/abs/2605.11369v1)
  - [Glove2Hand: Synthesizing Natural Hand-Object Interaction from Multi-Modal Sensing Gloves](http://arxiv.org/abs/2603.20850v1)
  - [ReMoGen: Real-time Human Interaction-to-Reaction Generation via Modular Learning from Diverse Data](http://arxiv.org/abs/2604.01082v1)
  - [Human Interaction-Aware 3D Reconstruction from a Single Image](http://arxiv.org/abs/2604.05436v1)
  - [A Dataset and Evaluation for Complex 4D Markerless Human Motion Capture](http://arxiv.org/abs/2604.12765v1)

### Multimodal Unlearning and Continual Distillation  _(N=56)_

このクラスターは、machine unlearning（特定データや敏感情報の部分削除）を中心に、knowledge distillation や test-time adaptation、continual learning を組み合わせてモデルの改変と継続的適応を同時に扱う点が特徴です。特に multimodal や long-tailed learning といった現実的なデータ課題に対する targeted unlearning やロバストな knowledge transfer 手法を提案する研究群が含まれます。

- **top keywords**: `machine unlearning`×4, `knowledge distillation`×4, `knowledge transfer`×3, `multimodal`×3, `continual learning`×3, `test-time adaptation`×3, `multimodal learning`×2, `long-tailed learning`×2
- **representative**:
  - [Designing to Forget: Deep Semi-parametric Models for Unlearning](http://arxiv.org/abs/2603.22870v1)
  - [SALMUBench: A Benchmark for Sensitive Association-Level Multimodal Unlearning](http://arxiv.org/abs/2603.26316v1)
  - [Multimodal Learning on Low-Quality Data with Conformal Predictive Self-Calibration](http://arxiv.org/abs/2605.03820v1)
  - [Reframing Long-Tailed Learning via Loss Landscape Geometry](http://arxiv.org/abs/2603.21217v1)
  - [Test-Time Distillation for Continual Model Adaptation](http://arxiv.org/abs/2506.02671v3)
  - [Class Unlearning via Depth-Aware Removal of Forget-Specific Directions](http://arxiv.org/abs/2604.15166v1)
  - [Purify-then-Align: Towards Robust Human Sensing under Modality Missing with Knowledge Distillation from Noisy Multimodal Teacher](http://arxiv.org/abs/2604.05584v2)
  - [RAZOR: Ratio-Aware Layer Editing for Targeted Unlearning in Vision Transformers and Diffusion Models](http://arxiv.org/abs/2603.14819v1)

### Efficient Tokenized Text-to-Video Diffusion  _(N=56)_

このクラスタは、text-to-video生成における長尺動画の時間的一貫性（temporal consistency）を保ちつつ、tokenizationやtoken compression、adaptive clusteringなどで計算効率を大幅に改善する研究群を含みます。特に diffusion models と transformer ベースのアーキテクチャに対して、sparse/streaming attention や adaptive token strategies によるO(n)級の効率化と長動画生成・編集の実用化を目指す点が特徴です。

- **top keywords**: `temporal consistency`×7, `text-to-video`×6, `temporal coherence`×5, `video diffusion`×5, `diffusion models`×4, `tokenization`×3, `video diffusion models`×3, `token compression`×3
- **representative**:
  - [LinVideo: A Post-Training Framework towards O(n) Attention in Efficient Video Generation](http://arxiv.org/abs/2510.08318v3)
  - [FrameDiT: Diffusion Transformer with Matrix Attention for Efficient Video Generation](http://arxiv.org/abs/2603.09721v2)
  - [Free-Lunch Long Video Generation via Layer-Adaptive O.O.D Correction](http://arxiv.org/abs/2603.25209v1)
  - [Mind the Generative Details: Direct Localized Detail Preference Optimization for Video Diffusion Models](http://arxiv.org/abs/2601.04068v3)
  - [VideoCoF: Unified Video Editing with Temporal Reasoner](http://arxiv.org/abs/2512.07469v2)
  - [EVATok: Adaptive Length Video Tokenization for Efficient Visual Autoregressive Generation](http://arxiv.org/abs/2603.12267v1)
  - [PoseGen: In-Context LoRA Finetuning for Pose-Controllable Long Human Video Generation](http://arxiv.org/abs/2508.05091v2)
  - [SwitchCraft: Training-Free Multi-Event Video Generation with Attention Controls](http://arxiv.org/abs/2602.23956v2)

### Adaptive Vision-Language Token Efficiency  _(N=55)_

このクラスターは、vision-language modelsの計算・通信コストを低減しつつ性能を維持するために、visual tokensの動的選択やtoken pruning、dynamic reweightingなどのAdaptiveな情報流制御を中心に扱う研究群です。trainingとinferenceの両面での効率化を図りつつ、zero-shot性能やadversarial robustness、継続学習の適応性も同時に向上させる点がユニークです。

- **top keywords**: `vision-language models`×8, `visual question answering`×4, `token pruning`×3, `zero-shot learning`×3, `multimodal`×3, `adversarial robustness`×3, `visual tokens`×3, `lifelong learning`×2
- **representative**:
  - [AdaptVision: Efficient Vision-Language Models via Adaptive Visual Acquisition](http://arxiv.org/abs/2512.03794v3)
  - [VISion On Request: Enhanced VLLM efficiency with sparse, dynamically selected, vision-language interactions](http://arxiv.org/abs/2603.23495v1)
  - [LLMind: Bio-inspired Training-free Adaptive Visual Representations for Vision-Language Models](http://arxiv.org/abs/2603.14882v2)
  - [Aligning What Vision-Language Models See and Perceive with Adaptive Information Flow](http://arxiv.org/abs/2604.15809v1)
  - [Variation-aware Vision Token Dropping for Faster Large Vision-Language Models](http://arxiv.org/abs/2509.01552v2)
  - [Dynamic Token Reweighting for Robust Vision-Language Models](http://arxiv.org/abs/2505.17132v3)
  - [Rethinking Model Selection in VLM Through the Lens of Gromov-Wasserstein Distance](http://arxiv.org/abs/2605.01325v1)
  - [Scaling Test-Time Robustness of Vision-Language Models via Self-Critical Inference Framework](http://arxiv.org/abs/2603.07659v2)

### 3D Asset Generation and Virtual Try-On  _(N=55)_

このクラスタは diffusion model や inpainting を核に、high-fidelityかつ editableな 3D assets と mesh generation を実現し、virtual try-on や immersive scene (VR) 向けの人物・都市・衣服表現を生成・編集する点に特化しています。text-image conditioning、point cloud priors、volume refinement といった手法を組み合わせ、promptable outfitting や効率的な 3D editing workflow を可能にする点が特徴です。

- **top keywords**: `virtual try-on`×5, `diffusion model`×4, `3d assets`×3, `diffusion models`×3, `inpainting`×3, `dataset`×3, `mesh generation`×3, `virtual reality`×2
- **representative**:
  - [Ar2Can: An Architect and an Artist Leveraging a Canvas for Multi-Human Generation](http://arxiv.org/abs/2511.22690v3)
  - [Text-Image Conditioned 3D Generation](http://arxiv.org/abs/2603.21295v1)
  - [Easy3E: Feed-Forward 3D Asset Editing via Rectified Voxel Flow](http://arxiv.org/abs/2602.21499v2)
  - [PROMO: Promptable Outfitting for Efficient High-Fidelity Virtual Try-On](http://arxiv.org/abs/2603.11675v1)
  - [Generative Texture Diversification of 3D Pedestrians for Robust Autonomous Driving Perception](http://arxiv.org/abs/2605.13755v1)
  - [REVIVE 3D: Refinement via Encoded Voluminous Inflated prior for Volume Enhancement](http://arxiv.org/abs/2604.27504v1)
  - [Points-to-3D: Structure-Aware 3D Generation with Point Cloud Priors](http://arxiv.org/abs/2603.18782v3)
  - [Stepper: Stepwise Immersive Scene Generation with Multiview Panoramas](http://arxiv.org/abs/2603.28980v2)

### Robust Forensics for AI-Generated Images  _(N=52)_

text-to-imageやdiffusion models由来のai-generated imagesやdeepfakeを対象に、adversarial attacksやドメイン変化に耐えるrobustでgeneralizableな検出・attribution・watermarking技術を中心に扱う。特にlocalizationやrecoveryを可能にするwatermarking、manifold deviationやrepresentation alignmentを用いたgeneralization改善、model-agnosticなattributionが特徴。

- **top keywords**: `text-to-image`×6, `robustness`×5, `diffusion models`×5, `deepfake detection`×5, `adversarial attacks`×4, `ai-generated images`×4, `watermarking`×4, `generalization`×3
- **representative**:
  - [Anti-I2V: Safeguarding your photos from malicious image-to-video generation](http://arxiv.org/abs/2603.24570v1)
  - [ReAlign: Generalizable Image Forgery Detection via Reasoning-Aligned Representation](http://arxiv.org/abs/2605.16080v1)
  - [Detecting AI-Generated Forgeries via Iterative Manifold Deviation Amplification](http://arxiv.org/abs/2602.18842v1)
  - [All in One: Unifying Deepfake Detection, Tampering Localization, and Source Tracing with a Robust Landmark-Identity Watermark](http://arxiv.org/abs/2602.23523v1)
  - [FRAME: Forensic Routing and Adaptive Multi-path Evidence Fusion for Image Manipulation Detection](http://arxiv.org/abs/2605.12826v1)
  - [SimLBR: Learning to Detect Fake Images by Learning to Detect Real Images](http://arxiv.org/abs/2602.20412v1)
  - [Layer Consistency Matters: Elegant Latent Transition Discrepancy for Generalizable Synthetic Image Detection](http://arxiv.org/abs/2603.10598v2)
  - [TriDF: Evaluating Perception, Detection, and Hallucination for Interpretable DeepFake Detection](http://arxiv.org/abs/2512.10652v3)

### 3D Gaussian Splatting for Scene Reconstruction  _(N=51)_

このクラスターは3D Gaussian Splattingを中心に、NeRFに代わる効率的な表現として高速な novel view synthesis や高精度な surface reconstruction、segmentation を目指す研究群です。Geometry priors、Neural Gabor、SLAM 統合や progressive filtering といった手法的工夫で実用性と品質の両立を図っている点が特徴です。

- **top keywords**: `3d gaussian splatting`×33, `gaussian splatting`×11, `scene reconstruction`×4, `novel view synthesis`×3, `semantic consistency`×2, `surface reconstruction`×2, `neural radiance fields`×2, `photorealistic rendering`×2
- **representative**:
  - [NG-GS: NeRF-Guided 3D Gaussian Splatting Segmentation](http://arxiv.org/abs/2604.14706v1)
  - [Off The Grid: Detection of Primitives for Feed-Forward 3D Gaussian Splatting](http://arxiv.org/abs/2512.15508v2)
  - [AnchorSplat: Feed-Forward 3D Gaussian Splatting with 3D Geometric Priors](http://arxiv.org/abs/2604.07053v2)
  - [Generalizable Human Gaussian Splatting via Multi-view Semantic Consistency](http://arxiv.org/abs/2604.25466v1)
  - [GaussFusion: Improving 3D Reconstruction in the Wild with A Geometry-Informed Video Generator](http://arxiv.org/abs/2603.25053v2)
  - [Neural Gabor Splatting: Enhanced Gaussian Splatting with Neural Gabor for High-frequency Surface Reconstruction](http://arxiv.org/abs/2604.15941v1)
  - [SGAD-SLAM: Splatting Gaussians at Adjusted Depth for Better Radiance Fields in RGBD SLAM](http://arxiv.org/abs/2603.21055v1)
  - [Using Gaussian Splats to Create High-Fidelity Facial Geometry and Texture](http://arxiv.org/abs/2512.16397v1)

### Concept Manipulation for Text-to-Image Diffusion Models  _(N=51)_

このクラスタはtext-to-image向けのdiffusion modelsにおける概念の導入・消去・分離と、その精密な編集やパーソナライズ化を扱う研究群です。Attentionやprompt blending、inversion、residual token optimizationといった手法を用いて、局所的な概念制御やトレーニング不要の操作、敵対的なパーソナライゼーションを実現する点が特徴です。

- **top keywords**: `text-to-image`×24, `diffusion models`×17, `concept erasure`×6, `image editing`×5, `diffusion transformers`×4, `generative models`×3, `style transfer`×3, `vq-vae`×3
- **representative**:
  - [TAUE: Training-free Noise Transplant and Cultivation Diffusion Model](http://arxiv.org/abs/2511.02580v2)
  - [Adaptive Auxiliary Prompt Blending for Target-Faithful Diffusion Generation](http://arxiv.org/abs/2603.19158v1)
  - [TINA: Text-Free Inversion Attack for Unlearned Text-to-Image Diffusion Models](http://arxiv.org/abs/2603.17828v1)
  - [Attention, May I Have Your Decision? Localizing Generative Choices in Diffusion Models](http://arxiv.org/abs/2604.06052v1)
  - [Beyond Text Prompts: Precise Concept Erasure through Text-Image Collaboration](http://arxiv.org/abs/2604.15829v1)
  - [ConceptPrism: Concept Disentanglement in Personalized Diffusion Models via Residual Token Optimization](http://arxiv.org/abs/2602.19575v2)
  - [ADAPT: Attention Driven Adaptive Prompt Scheduling and InTerpolating Orthogonal Complements for Rare Concepts Generation](http://arxiv.org/abs/2603.19157v1)
  - [Adversarial Concept Distillation for One-Step Diffusion Personalization](http://arxiv.org/abs/2510.20512v2)

### Interpretable and Sparse Vision Transformers  _(N=49)_

このクラスタはVision Transformer（ViT）の内部表現解析とtokenレベルのスパース性や圧縮を軸に、self-supervised学習やconcept-guided fine-tuningを用いて解釈性と効率性を高める研究群です。特にopen-vocabulary segmentationやanomaly detection、out-of-distribution検出といった応用タスクで、内部のlatent構造を活かして堅牢性や汎化を改善する点が特徴的です。

- **top keywords**: `vision transformers`×11, `interpretability`×5, `transformer`×5, `vision transformer`×4, `self-supervised`×4, `vision foundation models`×3, `semantic segmentation`×3, `sparse autoencoders`×2
- **representative**:
  - [Vision Transformers Need More Than Registers](http://arxiv.org/abs/2602.22394v2)
  - [Concept-Guided Fine-Tuning: Steering ViTs away from Spurious Correlations to Improve Robustness](http://arxiv.org/abs/2603.08309v2)
  - [Interpretable Vision Transformers in Monocular Depth Estimation via SVDA](http://arxiv.org/abs/2602.11005v1)
  - [SPAR: Single-Pass Any-Resolution ViT for Open-vocabulary Segmentation](http://arxiv.org/abs/2604.02252v1)
  - [Finding Distributed Object-Centric Properties in Self-Supervised Transformers](http://arxiv.org/abs/2603.26127v1)
  - [VisualAD: Language-Free Zero-Shot Anomaly Detection via Vision Transformer](http://arxiv.org/abs/2603.07952v1)
  - [Sparsity as a Key: Unlocking New Insights from Latent Structures for Out-of-Distribution Detection](http://arxiv.org/abs/2604.26409v1)
  - [SToRe3D: Sparse Token Relevance in ViTs for Efficient Multi-View 3D Object Detection](http://arxiv.org/abs/2605.14110v1)

### Molecularly-Guided Multimodal Medical Representation Learning  _(N=47)_

このクラスターは spatial transcriptomics や gene expression といった分子データを brain MRI や whole-slide image 等の医療画像と統合し、multimodal representation learning や foundation model、graph contrastive learning を用いて空間的・分子的な関係を推定・転移学習する研究群です。特徴は missing modalities や radiology reports を含む異種データの融合、anatomy-guided priors や intervention-aware 学習で臨床タスク（tumor segmentation、subtype classification、prognosis、disease recognition）に分子レベルの情報を反映する点です。

- **top keywords**: `spatial transcriptomics`×4, `brain tumor`×3, `multimodal`×3, `gene expression`×3, `brain mri`×2, `alzheimer's disease`×2, `chest x-ray`×2, `radiology reports`×2
- **representative**:
  - [CARE: A Molecular-Guided Foundation Model with Adaptive Region Modeling for Whole Slide Image Analysis](http://arxiv.org/abs/2602.21637v3)
  - [Cross-Slice Knowledge Transfer via Masked Multi-Modal Heterogeneous Graph Contrastive Learning for Spatial Gene Expression Inference](http://arxiv.org/abs/2603.22821v1)
  - [Can We Go Beyond Visual Features? Neural Tissue Relation Modeling for Relational Graph Analysis in Non-Melanoma Skin Histology](http://arxiv.org/abs/2512.06949v3)
  - [Uni-Encoder Meets Multi-Encoders: Representation Before Fusion for Brain Tumor Segmentation with Missing Modalities](http://arxiv.org/abs/2604.22177v1)
  - [AGA3DNet: Anatomy-Guided Gaussian Priors with Multi-view xLSTM for 3D Brain MRI Subtype Classification](http://arxiv.org/abs/2605.07142v1)
  - [Sparse Task Vector Mixup with Hypernetworks for Efficient Knowledge Transfer in Whole-Slide Image Prognosis](http://arxiv.org/abs/2603.10526v1)
  - [Toward Generalizable Whole Brain Representations with High-Resolution Light-Sheet Data](http://arxiv.org/abs/2603.29842v1)
  - [CheXmix: Unified Generative Pretraining for Vision Language Models in Medical Imaging](http://arxiv.org/abs/2604.22989v1)

### Multimodal Benchmarking for Vision-Language Models  _(N=45)_

このクラスタはbenchmarkを中心に、multimodal large language modelsやvision-language modelsの性能をaudio、video、graph、HOI、micro-action、editingといった多様なタスク横断で評価する研究群を含む。特徴は自動生成ベンチマークやscene-aware long-video評価、multi-agent strategic ability testingなど、実世界志向で細粒度な評価軸を体系化している点である。

- **top keywords**: `benchmark`×12, `multimodal`×8, `multimodal large language models`×7, `vision-language models`×5, `dataset`×3, `model evaluation`×2, `multi-modal`×2, `multimodal tasks`×2
- **representative**:
  - [See, Hear, and Understand: Benchmarking Audiovisual Human Speech Understanding in Multimodal Large Language Models](http://arxiv.org/abs/2512.02231v2)
  - [HumanVBench: Probing Human-Centric Video Understanding in MLLMs with Automatically Synthesized Benchmarks](http://arxiv.org/abs/2412.17574v3)
  - [VS-Bench: Evaluating VLMs for Strategic Abilities in Multi-Agent Environments](http://arxiv.org/abs/2506.02387v3)
  - [VEBench:Benchmarking Large Multimodal Models for Real-World Video Editing](http://arxiv.org/abs/2605.03276v2)
  - [GraphVLM: Benchmarking Vision Language Models for Multimodal Graph Learning](http://arxiv.org/abs/2603.13370v1)
  - [VISTA: Video Interaction Spatio-Temporal Analysis Benchmark](http://arxiv.org/abs/2605.01391v1)
  - [MA-Bench: Towards Fine-grained Micro-Action Understanding](http://arxiv.org/abs/2603.26586v1)
  - [AVA-Bench: Atomic Visual Ability Benchmark for Vision Foundation Models](http://arxiv.org/abs/2506.09082v5)

### 3D Spatial Reasoning in Vision-Language Models  _(N=45)_

このクラスターはVision-Language ModelsやMultimodal Modelsにおける空間推論能力、特に3D spatial reasoningやvisual perspective takingの評価と改善を目的とした研究群である。BEV-groundingやchain-of-thoughtを活用したモデル設計やSpatiaLQAなどのbenchmark構築、zero-shot navigationやspatial logical reasoningを扱う評価指標の提案を通じて、spatial intelligenceの計測・強化に焦点を当てている。

- **top keywords**: `spatial reasoning`×12, `vision-language models`×6, `zero-shot navigation`×3, `benchmark`×3, `3d spatial reasoning`×3, `large language models`×3, `spatial intelligence`×3, `multimodal models`×2
- **representative**:
  - [HiSpatial: Taming Hierarchical 3D Spatial Understanding in Vision-Language Models](http://arxiv.org/abs/2603.25411v1)
  - [EgoMind: Activating Spatial Cognition through Linguistic Reasoning in MLLMs](http://arxiv.org/abs/2604.03318v1)
  - [EagleVision: A Dual-Stage Framework with BEV-grounding-based Chain-of-Thought for Spatial Intelligence](http://arxiv.org/abs/2512.15160v2)
  - [Beyond Recognition: Evaluating Visual Perspective Taking in Vision Language Models](http://arxiv.org/abs/2505.03821v2)
  - [SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models](http://arxiv.org/abs/2602.20901v1)
  - [BOP-ASK: Object-Interaction Reasoning for Vision-Language Models](http://arxiv.org/abs/2511.16857v3)
  - [Learning Multi-View Spatial Reasoning from Cross-View Relations](http://arxiv.org/abs/2603.27967v1)
  - [Masking Matters: Unlocking the Spatial Reasoning Capabilities of LLMs for 3D Scene-Language Understanding](http://arxiv.org/abs/2512.02487v2)

### Reinforcement-Guided Multimodal Video Reasoning  _(N=44)_

このクラスターはreinforcement learningを組み合わせてchain-of-thoughtやagentic reasoningを強化し、multimodal LLMsで長尺のvideo understandingやvisual/multimodal reasoningを行う研究群を含む。hierarchical memoryやactive visual perceptionといった構造を導入して、長時間・関係性重視の動画推論をベンチマーク上で改善する点が特徴である。

- **top keywords**: `reinforcement learning`×12, `chain-of-thought`×7, `video reasoning`×6, `multimodal reasoning`×6, `visual reasoning`×5, `multimodal models`×4, `benchmark`×4, `video understanding`×4
- **representative**:
  - [Reinforce to Learn, Elect to Reason: A Dual Paradigm for Video Reasoning](http://arxiv.org/abs/2604.04379v1)
  - [Chain-of-Frames: Advancing Video Understanding in Multimodal LLMs via Frame-Aware Reasoning](http://arxiv.org/abs/2506.00318v2)
  - [OneThinker: All-in-one Reasoning Model for Image and Video](http://arxiv.org/abs/2512.03043v3)
  - [VRR-QA: Visual Relational Reasoning in Videos Beyond Explicit Cues](http://arxiv.org/abs/2506.21742v3)
  - [VideoARM: Agentic Reasoning over Hierarchical Memory for Long-Form Video Understanding](http://arxiv.org/abs/2512.12360v2)
  - [VIDEOP2R: Video Understanding from Perception to Reasoning](http://arxiv.org/abs/2511.11113v2)
  - [AVATAR: Reinforcement Learning to See, Hear, and Reason Over Video](http://arxiv.org/abs/2508.03100v4)
  - [Reinforcing Structured Chain-of-Thought for Video Understanding](http://arxiv.org/abs/2603.25942v1)

### CLIP-based Cross-Domain Few-Shot Adaptation  _(N=43)_

CLIPを中心としたvision-language表現を利用し、few-shot／zero-shotやsource-freeのcross-domain適応とopen-vocabulary segmentationなど実用タスクへの転用を目指す研究群です。特徴はCLIP表現の局所・グローバル整合やstructured geometric transformation、concept-based説明といった手法でdomain generalizationとデータ効率を高める点です。

- **top keywords**: `clip`×23, `few-shot learning`×6, `vision-language models`×3, `zero-shot`×3, `cross-domain`×3, `domain generalization`×2, `concept bottleneck models`×2, `zero-shot retrieval`×2
- **representative**:
  - [MedCLIPSeg: Probabilistic Vision-Language Adaptation for Data-Efficient and Generalizable Medical Image Segmentation](http://arxiv.org/abs/2602.20423v1)
  - [BiCLIP: Domain Canonicalization via Structured Geometric Transformation](http://arxiv.org/abs/2603.08942v2)
  - [CLIP Is Shortsighted: Paying Attention Beyond the First Sentence](http://arxiv.org/abs/2602.22419v2)
  - [Looking Beyond the Window: Global-Local Aligned CLIP for Training-free Open-Vocabulary Semantic Segmentation](http://arxiv.org/abs/2603.23030v1)
  - [SRL-CLIP: Efficient CLIP Video Adaptation via Structured Semantic Role Labels](http://arxiv.org/abs/2401.07669v2)
  - [Interpretable Cross-Domain Few-Shot Learning with Rectified Target-Domain Local Alignment](http://arxiv.org/abs/2603.17655v2)
  - [CLIPoint3D: Language-Grounded Few-Shot Unsupervised 3D Point Cloud Domain Adaptation](http://arxiv.org/abs/2602.20409v2)
  - [Multimodal Causal-Driven Representation Learning for Generalizable Medical Image Segmentation](http://arxiv.org/abs/2508.05008v2)

### 4D Gaussian Splatting for Dynamic Scenes  _(N=42)_

このクラスタは3D/4D Gaussian Splattingを中心に、dynamic scenesのAppearance、Geometry、Motionを高精度に再構成・生成する研究群です。monocular videosやsparse camerasからの4D復元、temporal consistency保持、open-vocabularyな3D理解、および高速・オンライン推論や制御可能なシーン合成に重点を置いています。

- **top keywords**: `3d gaussian splatting`×8, `dynamic scenes`×6, `3d scene generation`×3, `4d gaussian splatting`×3, `monocular videos`×3, `open-vocabulary`×3, `temporal consistency`×3, `dynamic gaussian splatting`×2
- **representative**:
  - [MotionScale: Reconstructing Appearance, Geometry, and Motion of Dynamic Scenes with Scalable 4D Gaussian Splatting](http://arxiv.org/abs/2603.29296v1)
  - [Diff4Splat: Controllable 4D Scene Generation with Latent Dynamic Reconstruction Models](http://arxiv.org/abs/2511.00503v2)
  - [4C4D: 4 Camera 4D Gaussian Splatting](http://arxiv.org/abs/2604.04063v1)
  - [GRVS: a Generalizable and Recurrent Approach to Monocular Dynamic View Synthesis](http://arxiv.org/abs/2603.29734v1)
  - [MoVieS: Motion-Aware 4D Dynamic View Synthesis in One Second](http://arxiv.org/abs/2507.10065v2)
  - [Bringing a Personal Point of View: Evaluating Dynamic 3D Gaussian Splatting for Egocentric Scene Reconstruction](http://arxiv.org/abs/2604.23803v1)
  - [AeroDGS: Physically Consistent Dynamic Gaussian Splatting for Single-Sequence Aerial 4D Reconstruction](http://arxiv.org/abs/2602.22376v1)
  - [SparseCam4D: Spatio-Temporally Consistent 4D Reconstruction from Sparse Cameras](http://arxiv.org/abs/2603.26481v3)

### Mitigating Hallucinations in Vision-Language Models  _(N=42)_

このクラスタはvisual groundingやattention-guided strategies、contrastive decodingなどを駆使してVision-Language ModelsやLVLMsのhallucinationを検出・軽減する研究群です。multimodal reasoningやchain-of-thoughtの信頼性向上、visual tool reasoningやprefill-time interventionといった実用的な介入法でinterpretabilityとgroundingを強化する点が特徴です。

- **top keywords**: `visual grounding`×8, `hallucination mitigation`×7, `multimodal reasoning`×5, `multimodal`×4, `vision-language models`×3, `visual reasoning`×2, `interpretability`×2, `hallucination`×2
- **representative**:
  - [Residual Decoding: Mitigating Hallucinations in Large Vision-Language Models via History-Aware Residual Guidance](http://arxiv.org/abs/2602.01047v3)
  - [Mitigating Object Hallucinations in LVLMs via Attention Imbalance Rectification](http://arxiv.org/abs/2603.24058v1)
  - [Tell Model Where to Look: Mitigating Hallucinations in MLLMs by Vision-Guided Attention](http://arxiv.org/abs/2511.20032v3)
  - [3D-VCD: Hallucination Mitigation in 3D-LLM Embodied Agents through Visual Contrastive Decoding](http://arxiv.org/abs/2604.08645v1)
  - [Attention-space Contrastive Guidance for Efficient Hallucination Mitigation in LVLMs](http://arxiv.org/abs/2601.13707v2)
  - [Video-Only ToM: Enhancing Theory of Mind in Multimodal Large Language Models](http://arxiv.org/abs/2603.24484v1)
  - [Understanding and Mitigating Hallucinations in Multimodal Chain-of-Thought Models](http://arxiv.org/abs/2603.27201v1)
  - [Seeing Clearly, Reasoning Confidently: Plug-and-Play Remedies for Vision Language Model Blindness](http://arxiv.org/abs/2602.19615v1)

### Reward-Driven Alignment for Text-to-Image Generation  _(N=41)_

このクラスタはtext-to-imageやmultimodal generative modelsの生成品質・一貫性を向上させるために、reinforcement learningやreward modelingを用いてintrinsic/latent rewardsやpreference optimizationを設計する研究群です。特にdiffusion reinforcement learning、Pareto-optimal curriculumやpairwise subject-consistencyといった報酬設計によるsemantic/structural alignmentと多目的最適化を重視します。

- **top keywords**: `reinforcement learning`×19, `text-to-image`×7, `generative models`×3, `autoregressive models`×2, `large language models`×2, `multimodal large language models`×2, `semantic alignment`×2, `unified multimodal models`×2
- **representative**:
  - [Learning to Generate via Understanding: Understanding-Driven Intrinsic Rewarding for Unified Multimodal Models](http://arxiv.org/abs/2603.06043v1)
  - [Enhancing Spatial Understanding in Image Generation via Reward Modeling](http://arxiv.org/abs/2602.24233v1)
  - [MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models](http://arxiv.org/abs/2511.20629v5)
  - [Taming Preference Mode Collapse via Directional Decoupling Alignment in Diffusion Reinforcement Learning](http://arxiv.org/abs/2512.24146v2)
  - [TextPecker: Rewarding Structural Anomaly Quantification for Enhancing Visual Text Rendering](http://arxiv.org/abs/2602.20903v3)
  - [POCA: Pareto-Optimal Curriculum Alignment for Visual Text Generation](http://arxiv.org/abs/2604.24171v1)
  - [Resolving the Identity Crisis in Text-to-Image Generation](http://arxiv.org/abs/2510.01399v3)
  - [PSR: Scaling Multi-Subject Personalized Image Generation with Pairwise Subject-Consistency Rewards](http://arxiv.org/abs/2512.01236v2)

### Flow Matching for Motion and Generation  _(N=32)_

このクラスタはflow matchingやoptical flowを基盤に、video motion transfer、text-to-motion、single-step neural renderingなどの動き生成・可視化タスクを扱う研究群です。diffusion modelsやtrajectory-based formulationsをflowベースで再解釈し、training-free guidanceやreinforcement learning/ reward optimization、velocity contrastive regularizationといった手法で効率的かつスケーラブルに運動・流れを生成・制御する点が特徴です。

- **top keywords**: `flow matching`×6, `optical flow`×5, `flow-matching`×3, `semantic alignment`×3, `motion generation`×2, `diffusion models`×2, `reinforcement learning`×2, `training-free`×2
- **representative**:
  - [Flow3r: Factored Flow Prediction for Scalable Visual Geometry Learning](http://arxiv.org/abs/2602.20157v1)
  - [FlowMotion: Training-Free Flow Guidance for Video Motion Transfer](http://arxiv.org/abs/2603.06289v2)
  - [RewardFlow: Generate Images by Optimizing What You Reward](http://arxiv.org/abs/2604.08536v1)
  - [RenderFlow: Single-Step Neural Rendering via Flow Matching](http://arxiv.org/abs/2601.06928v2)
  - [LeapAlign: Post-Training Flow Matching Models at Any Generation Step by Building Two-Step Trajectories](http://arxiv.org/abs/2604.15311v2)
  - [From Navigation to Refinement: Revealing the Two-Stage Nature of Flow-based Diffusion Models through Oracle Velocity](http://arxiv.org/abs/2512.02826v3)
  - [Rethinking Dense Optical Flow without Test-Time Scaling](http://arxiv.org/abs/2605.08000v1)
  - [EgoFlow: Gradient-Guided Flow Matching for Egocentric 6DoF Object Motion Generation](http://arxiv.org/abs/2604.01421v1)

### Real-World Image Restoration and Perceptual Evaluation  _(N=31)_

このクラスターは real-world image restoration の benchmark、dataset、challenge 結果といった評価基盤と、perceptual quality や image quality assessment を測る新しい evaluation metrics に焦点を当てている。特徴は ground truth 比較だけでない評価（partial-reference/NR-IQA や perception gap の議論）や、super-resolution を含む現実劣化下での手法比較とメトリクス改善にある。

- **top keywords**: `image restoration`×7, `benchmark`×4, `image quality assessment`×4, `perceptual quality`×4, `super-resolution`×3, `real-world degradation`×2, `dataset`×2, `evaluation metrics`×2
- **representative**:
  - [Beyond Ground-Truth: Leveraging Image Quality Priors for Real-World Image Restoration](http://arxiv.org/abs/2603.29773v2)
  - [NTIRE 2026 The 3rd Restore Any Image Model (RAIM) Challenge: AI Flash Portrait (Track 3)](http://arxiv.org/abs/2604.11230v1)
  - [LoViF 2026 Challenge on Real-World All-in-One Image Restoration: Methods and Results](http://arxiv.org/abs/2604.19445v1)
  - [The Second Challenge on Real-World Face Restoration at NTIRE 2026: Methods and Results](http://arxiv.org/abs/2604.10532v2)
  - [Beyond the Ground Truth: Enhanced Supervision for Image Restoration](http://arxiv.org/abs/2512.03932v3)
  - [PR-IQA: Partial-Reference Image Quality Assessment for Diffusion-Based Novel View Synthesis](http://arxiv.org/abs/2604.04576v2)
  - [Bridging the Perception Gap in Image Super-Resolution Evaluation](http://arxiv.org/abs/2503.13074v3)
  - [Benchmarking Endoscopic Surgical Image Restoration and Beyond](http://arxiv.org/abs/2505.19161v3)

### Vision-Language-Action for Robotic Manipulation  _(N=30)_

このクラスタはvision-language-actionモデルを中心に、robotic manipulationのための効率的かつ長期的なpolicy learningとplanningを扱う研究群です。特徴はsample efficiencyやknowledge graphを活用したreasoning、verbalizable latent planningやAction Chain-of-Thought的推論、affordance reasoningやforce-aware control、simulation-enabled planningや4D spatiotemporal consistencyを組み合わせてcontact-richな実世界操作へ応用する点です。

- **top keywords**: `vision-language-action`×4, `robotic manipulation`×3, `manipulation`×3, `vision-language models`×3, `vla models`×2, `sample efficiency`×2, `knowledge graph`×2, `policy learning`×2
- **representative**:
  - [AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention](http://arxiv.org/abs/2511.18960v3)
  - [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](http://arxiv.org/abs/2601.09708v2)
  - [Learning to See and Act: Task-Aware Virtual View Exploration for Robotic Manipulation](http://arxiv.org/abs/2508.05186v5)
  - [ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models](http://arxiv.org/abs/2601.11404v2)
  - [SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models](http://arxiv.org/abs/2512.05955v2)
  - [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](http://arxiv.org/abs/2605.05126v1)
  - [NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning](http://arxiv.org/abs/2602.21172v2)
  - [PALM: Progress-Aware Policy Learning via Affordance Reasoning for Long-Horizon Robotic Manipulation](http://arxiv.org/abs/2601.07060v2)

### Multimodal Embodied Agent Planning  _(N=30)_

このクラスターは、embodied agents や GUI agents に対する長期的な task planning と行動選択を、reinforcement learning や multi-agent frameworks を用いて解く研究群です。collaborative policy planning、verifier-guided action selection、actionable memory や execution-feedback を組み合わせてマルチモーダル理解と自律的実行を結びつける点がユニークです。

- **top keywords**: `reinforcement learning`×5, `multimodal`×3, `gui agents`×3, `task planning`×2, `multimodal agents`×2, `multi-agent reinforcement learning`×2, `embodied agents`×2, `intent inference`×1
- **representative**:
  - [RoboAgent: Chaining Basic Capabilities for Embodied Task Planning](http://arxiv.org/abs/2604.07774v1)
  - [VideoChat-M1: Collaborative Policy Planning for Video Understanding via Multi-Agent Reinforcement Learning](http://arxiv.org/abs/2511.19524v2)
  - [Anticipatory Planning for Multimodal AI Agents](http://arxiv.org/abs/2603.16777v1)
  - [CompAgent: An Agentic Framework for Visual Compliance Verification](http://arxiv.org/abs/2511.00171v3)
  - [Think Twice, Act Once: Verifier-Guided Action Selection For Embodied Agents](http://arxiv.org/abs/2605.12620v1)
  - [Environmental Understanding Vision-Language Model for Embodied Agent](http://arxiv.org/abs/2604.19839v1)
  - [HATS: Hardness-Aware Trajectory Synthesis for GUI Agents](http://arxiv.org/abs/2603.12138v1)
  - [CarePilot: A Multi-Agent Framework for Long-Horizon Computer Task Automation in Healthcare](http://arxiv.org/abs/2603.24157v1)

### Hardware-Aware Quantization and PEFT for Edge Generative Models  _(N=29)_

このクラスタはhardware-awareなquantizationとparameter-efficient fine-tuning（PEFT）を組み合わせ、Diffusion Transformersやgenerative vision modelsを低リソースなedge devices上で効率的に動かす点が特徴です。mixed-precision attention、adaptive distillation、KV-Cache quantizationやtraining-free accelerationなど、ハードウェア制約に最適化された圧縮・実装・デプロイ技術に重点を置いています。

- **top keywords**: `edge devices`×4, `quantization`×3, `parameter-efficient fine-tuning`×3, `hardware-aware`×2, `quantization-aware training`×2, `generative ai`×2, `diffusion transformers`×2, `multi-task learning`×2
- **representative**:
  - [Flash-Unified: A Training-Free and Task-Aware Acceleration Framework for Native Unified Models](http://arxiv.org/abs/2603.15271v1)
  - [Decompose, Mix, Adapt: A Unified Framework for Parameter-Efficient Neural Network Recombination and Compression](http://arxiv.org/abs/2603.27383v2)
  - [Bridging the Training-Deployment Gap: Gated Encoding and Multi-Scale Refinement for Efficient Quantization-Aware Image Enhancement](http://arxiv.org/abs/2604.21743v1)
  - [Quantization with Unified Adaptive Distillation to enable multi-LoRA based one-for-all Generative Vision Models on edge](http://arxiv.org/abs/2603.29535v1)
  - [EdgeDiT: Hardware-Aware Diffusion Transformers for Efficient On-Device Image Generation](http://arxiv.org/abs/2603.28405v1)
  - [Diagonal-Tiled Mixed-Precision Attention for Efficient Low-Bit MXFP Inference](http://arxiv.org/abs/2604.03950v1)
  - [Hardware-Aware Neural Feature Extraction for Resource-Constrained Devices](http://arxiv.org/abs/2605.04282v2)
  - [AdaBet: Gradient-free Layer Selection for Efficient Training of Deep Neural Networks](http://arxiv.org/abs/2510.03101v2)

### Scalable End-to-End Driving with Latent World Models  _(N=29)_

このクラスタは、trajectory predictionやimitation learningを軸に、large-scale synthetic dataやself-supervised pretrainingを活用してend-to-end drivingをスケール・安定化する研究群です。simulation-driven dataset generation、latent world models、closed-loop evaluationを組み合わせ、proactive planningやfine-grained safety reasoningを導入してrobustな motion planning/trajectory planning を学習する点が特徴です。

- **top keywords**: `trajectory prediction`×4, `imitation learning`×3, `trajectory planning`×2, `dataset generation`×2, `motion planning`×2, `self-supervised learning`×2, `synthetic data`×2, `end-to-end driving`×2
- **representative**:
  - [SimScale: Learning to Drive via Real-World Simulation at Scale](http://arxiv.org/abs/2511.23369v3)
  - [ProDrive: Proactive Planning for Autonomous Driving via Ego-Environment Co-Evolution](http://arxiv.org/abs/2604.25329v1)
  - [What Matters for Scalable and Robust Learning in End-to-End Driving Planners?](http://arxiv.org/abs/2603.15185v1)
  - [SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World](http://arxiv.org/abs/2602.18887v2)
  - [HorizonWeaver: Generalizable Multi-Level Semantic Editing for Driving Scenes](http://arxiv.org/abs/2604.04887v1)
  - [DriveLaW:Unifying Planning and Video Generation in a Latent Driving World](http://arxiv.org/abs/2512.23421v3)
  - [Learning to Drive is a Free Gift: Large-Scale Label-Free Autonomy Pretraining from Unposed In-The-Wild Videos](http://arxiv.org/abs/2602.22091v2)
  - [DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving](http://arxiv.org/abs/2604.00969v1)

### Adaptive Multimodal Tracking and Test-Time Adaptation  _(N=28)_

このクラスタは、test-time adaptationやdynamic network parameter adaptationを駆使して、multimodal（RGB、point cloud、language）入力でリアルタイムかつロバストなmulti-objectおよびpoint trackingを実現する研究群を含む。特にtemporal priors、long-term memory、occlusion handling、referring multi-object trackingやopen-set耐性といった時間的一貫性と適応性の向上に重きを置いている点が特徴。

- **top keywords**: `test-time adaptation`×5, `transformer`×2, `real-time tracking`×2, `occlusion handling`×2, `referring multi-object tracking`×2, `multi-object tracking`×2, `multimodal`×2, `open-set`×1
- **representative**:
  - [SEATrack: Simple, Efficient, and Adaptive Multimodal Tracker](http://arxiv.org/abs/2604.12502v1)
  - [Drift-Resilient Temporal Priors for Visual Tracking](http://arxiv.org/abs/2604.02654v1)
  - [CD-Buffer: Complementary Dual-Buffer Framework for Test-Time Adaptation in Adverse Weather Object Detection](http://arxiv.org/abs/2603.26092v1)
  - [AnthroTAP: Learning Point Tracking with Real-World Motion](http://arxiv.org/abs/2507.06233v3)
  - [Adapting Point Cloud Analysis via Multimodal Bayesian Distribution Learning](http://arxiv.org/abs/2603.22070v2)
  - [Temporally Consistent Long-Term Memory for 3D Single Object Tracking](http://arxiv.org/abs/2604.13789v1)
  - [From Pairs to Sequences: Track-Aware Policy Gradients for Keypoint Detection](http://arxiv.org/abs/2602.20630v4)
  - [Rethinking Two-Stage Referring-by-Tracking in Referring Multi-Object Tracking: Make it Strong Again](http://arxiv.org/abs/2503.07516v5)

### Physics-Aware Video and Motion Generation  _(N=24)_

このクラスタは物理知識を明示的に組み込んだphysics-aware／physics-infused手法で、物理的に一貫した動的動画と制御可能な generative motion を生成する研究群です。physics-supervised 学習や physical simulator in-the-loop、video diffusion や ControlNet 等の local conditioning を組み合わせて、物理制約下での予測・プランニングやロボットデモ生成まで扱う点がユニークです。

- **top keywords**: `physics-aware`×3, `motion generation`×3, `video generation`×3, `physically consistent`×1, `generative motion`×1, `video diffusion`×1, `controlnet`×1, `physics-supervised`×1
- **representative**:
  - [Phantom: Physics-Infused Video Generation via Joint Modeling of Visual and Latent Physical Dynamics](http://arxiv.org/abs/2604.08503v2)
  - [PhyCo: Learning Controllable Physical Priors for Generative Motion](http://arxiv.org/abs/2604.28169v1)
  - [PhysVid: Physics Aware Local Conditioning for Generative Video Models](http://arxiv.org/abs/2603.26285v2)
  - [Physical Simulator In-the-Loop Video Generation](http://arxiv.org/abs/2603.06408v1)
  - [DynaVid: Learning to Generate Highly Dynamic Videos using Synthetic Motion Data](http://arxiv.org/abs/2604.01666v1)
  - [Image Generation as a Visual Planner for Robotic Manipulation](http://arxiv.org/abs/2512.00532v1)
  - [Goal Force: Teaching Video Models To Accomplish Physics-Conditioned Goals](http://arxiv.org/abs/2601.05848v2)
  - [Envisioning the Future, One Step at a Time](http://arxiv.org/abs/2604.09527v1)

### Personalized and Efficient Federated Learning  _(N=23)_

このクラスタは federated learning の現実的課題（model heterogeneity、data heterogeneity、global class imbalance、domain shift）に対応しつつ、personalized federated learning と communication/computation efficiency を両立する手法群を含みます。さらに privacy-preserving や federated unlearning、efficient submodel extraction、multimodal aggregation といった実運用を見据えた汎用性と頑健性に重点を置いている点が特徴です。

- **top keywords**: `federated learning`×6, `data heterogeneity`×3, `personalized federated learning`×2, `privacy-preserving`×2, `cifar-10`×2, `class imbalance`×2, `privacy protection`×2, `communication efficiency`×2
- **representative**:
  - [FedRE: A Representation Entanglement Framework for Model-Heterogeneous Federated Learning](http://arxiv.org/abs/2511.22265v2)
  - [FedAFD: Multimodal Federated Learning via Adversarial Fusion and Distillation](http://arxiv.org/abs/2603.04890v1)
  - [FedDAP: Domain-Aware Prototype Learning for Federated Learning under Domain Shift](http://arxiv.org/abs/2604.06795v1)
  - [FedVG: Gradient-Guided Aggregation for Enhanced Federated Learning](http://arxiv.org/abs/2602.21399v2)
  - [FedSIR: Spectral Client Identification and Relabeling for Federated Learning with Noisy Labels](http://arxiv.org/abs/2604.20825v1)
  - [Federated Active Learning Under Extreme Non-IID and Global Class Imbalance](http://arxiv.org/abs/2603.10341v1)
  - [Single-Round Scalable Analytic Federated Learning](http://arxiv.org/abs/2512.03336v2)
  - [Fine-Tuning Impairs the Balancedness of Foundation Models in Long-tailed Personalized Federated Learning](http://arxiv.org/abs/2605.02247v1)

### Animatable 3D Gaussian Head Avatars  _(N=14)_

Gaussian splattingやhigh-dimensional Gaussian representationsを用いて、高精度なanimatable 3D head/face avatarsを復元・レンダリングする研究群です。monocular videosやmulti-view dataからの学習、blendshapesやtemporal density controlによるアニメーション制御、mobileやreal-time向けの軽量化・streaming diffusionを含む生成・配信手法までを扱う点が特徴です。

- **top keywords**: `3d head avatars`×3, `3d gaussian`×2, `animatable avatars`×2, `monocular videos`×2, `high-fidelity avatars`×1, `mobile devices`×1, `blendshapes`×1, `multi-view video`×1
- **representative**:
  - [HyperGaussians: High-Dimensional Gaussian Splatting for High-Fidelity Animatable Face Avatars](http://arxiv.org/abs/2507.02803v3)
  - [Motion-Aware Animatable Gaussian Avatars Deblurring](http://arxiv.org/abs/2411.16758v3)
  - [AvatarPointillist: AutoRegressive 4D Gaussian Avatarization](http://arxiv.org/abs/2604.04787v2)
  - [STAvatar: Soft Binding and Temporal Density Control for Monocular 3D Head Avatars Reconstruction](http://arxiv.org/abs/2511.19854v3)
  - [FlexAvatar: Learning Complete 3D Head Avatars with Partial Supervision](http://arxiv.org/abs/2512.15599v2)
  - [ProgressiveAvatars: Progressive Animatable 3D Gaussian Avatars](http://arxiv.org/abs/2603.16447v1)
  - [PhysHead: Simulation-Ready Gaussian Head Avatars](http://arxiv.org/abs/2604.06467v1)
  - [High-Fidelity Mobile Avatars with Pruned Local Blendshapes](http://arxiv.org/abs/2605.01854v1)

### Subspace-Aware and Robust Model Merging  _(N=11)_

このクラスターは、model merging を essential subspace や subspace-aware 手法で行い、task-feature specialization を保ちつつ directional anisotropy や weight disentanglement の課題に対処する研究群です。LoRA merging、null-space compression、orthogonality 制約や mixture-of-experts 特化強化を組み合わせて、マルチタスクやクロスドメインでの安全かつ高性能なモデル統合を目指す点が特徴です.

- **top keywords**: `model merging`×6, `multi-task learning`×4, `task arithmetic`×1, `weight disentanglement`×1, `task-feature specialization`×1, `orthoreg`×1, `orthogonality`×1, `mixture-of-experts`×1
- **representative**:
  - [Model Merging in the Essential Subspace](http://arxiv.org/abs/2602.20208v1)
  - [Bridging Domains through Subspace-Aware Model Merging](http://arxiv.org/abs/2603.05768v2)
  - [DC-Merge: Improving Model Merging with Directional Consistency](http://arxiv.org/abs/2603.06242v2)
  - [Defending Unauthorized Model Merging via Dual-Stage Weight Protection](http://arxiv.org/abs/2511.11851v3)
  - [Preference-Aligned LoRA Merging: Preserving Subspace Coverage and Addressing Directional Anisotropy](http://arxiv.org/abs/2603.26299v1)
  - [BD-Merging: Bias-Aware Dynamic Model Merging with Evidence-Guided Contrastive Learning](http://arxiv.org/abs/2603.03920v2)
  - [Label-Free Cross-Task LoRA Merging with Null-Space Compression](http://arxiv.org/abs/2603.26317v1)
  - [MOMO: Mars Orbital Model Foundation Model for Mars Orbital Applications](http://arxiv.org/abs/2604.02719v1)

## 4. LLM 俯瞰分析

以下は条件付けカテゴリを使わず、`gpt-5-mini` に title + task_keywords + track の全件リストを渡して「現場のトレンド」を抽出させた結果。

### 4.1 新興テーマ

**3D Gaussian Splatting and 4D / dynamic neural rendering**

CVPR 2026では3D Gaussian Splatting（およびその4D / dynamic extension）関連の研究が非常に目立つ。dynamic scene reconstruction, avatar/face/head rendering, uncertainty-aware and physics-guided variantsまで幅広く扱われ、NeRFやNeRF-guided手法と併用する研究も散見される。リアルタイム性・効率化（fast fitting / sparse lists / feed-forward）と時間的一貫性（4D, temporal coherence）を同時に扱う論文が多い点が特徴。

代表的なタイトル:
- GP-4DGS: Probabilistic 4D Gaussian Splatting from Monocular Video via Variational Gaussian Processes
- MotionScale: Reconstructing Appearance, Geometry, and Motion of Dynamic Scenes with Scalable 4D Gaussian Splatting
- 4C4D: 4 Camera 4D Gaussian Splatting
- ProgressiveAvatars: Progressive Animatable 3D Gaussian Avatars
- VarSplat: Uncertainty-aware 3D Gaussian Splatting for Robust RGB-D SLAM

**Multimodal Large Language Models / Vision-Language Models for spatial & temporal reasoning and embodied agents**

VLMs / MLLMs を spatial, temporal, embodied tasks に組み込む研究が多く観測される。エゴセントリック理解、navigation, embodied manipulation、long-video reasoningやchain-of-thought／agenticフレームワークを組み合わせた応用が散見され、視覚と言語の空間的結びつけ（3D grounding, scene graph, affordance grounding）が頻出。実システム（robotic planning, UAV, driving）との接続も目立つ。

代表的なタイトル:
- From Where Things Are to What They Are For: Benchmarking Spatial-Functional Intelligence in Multimodal LLMs
- RoboAgent: Chaining Basic Capabilities for Embodied Task Planning
- Environmental Understanding Vision-Language Model for Embodied Agent
- SpatialStack: Layered Geometry-Language Fusion for 3D VLM Spatial Reasoning
- Scaling the Long Video Understanding of Multimodal Large Language Models via Visual Memory Mechanism

**Diffusion & flow-matching methods pushed across modalities (image, video, motion, 3D) and sampling acceleration**

diffusion / flow-matching が画像生成に留まらず、text-to-motion, video, 3D generation, sampling-accelerationやclassifier-free guidanceの新手法と組み合わせて多用途化している。さらに『efficient / training-free / one-step』的な工夫（linear predictors, feature caching, Padé approximations, trajectory tricks）が頻出し、実用性と速度改善に強い関心がある。

代表的なタイトル:
- MotionHiFlow: Text-to-motion via hierarchical flow matching
- Beyond Fixed Formulas: Data-Driven Linear Predictor for Efficient Diffusion Models
- DA-VAE: Plug-in Latent Compression for Diffusion via Detail Alignment
- TC-Padé: Trajectory-Consistent Padé Approximation for Diffusion Acceleration
- Denoising, Fast and Slow: Difficulty-Aware Adaptive Sampling for Image Generation

**Open-vocabulary / zero-shot and foundation-model adaptation for 2D/3D perception**

open-vocabulary / zero-shotパラダイムを3Dやpanoptic/semantic tasksに拡張する論文が多い。training-freeやprototype / prompt-based手法で、open-vocabulary semantic segmentation / detection / 3D understanding を目指す研究群が散見される。CLIP/DINO系を用いた実用的なゼロショット化が目立つ。

代表的なタイトル:
- SPAR: Single-Pass Any-Resolution ViT for Open-vocabulary Segmentation
- PEARL: Geometry Aligns Semantics for Training-Free Open-Vocabulary Semantic Segmentation
- OpenDPR: Open-Vocabulary Change Detection via Vision-Centric Diffusion-Guided Prototype Retrieval for Remote Sensing Imagery
- Direct Segmentation without Logits Optimization for Training-Free Open-Vocabulary Semantic Segmentation
- ExtrinSplat: Decoupling Geometry and Semantics for Open-Vocabulary Understanding in 3D Gaussian Splatting

**Embodied perception-action, affordance reasoning and VLA (Vision-Language-Action) for robotics**

視覚と言語を結びつけたエージェントやVLA（vision-language-action）研究が多数見られる。grasp/affordance grounding、bimanual manipulation、sim-to-real、policy・planningと生成（world models, latent planners）を組み合わせる論文が散見され、ロボティクス応用を強く意識したラインが目立つ。

代表的なタイトル:
- UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos
- PALM: Progress-Aware Policy Learning via Affordance Reasoning for Long-Horizon Robotic Manipulation
- AffordMatcher: Affordance Learning in 3D Scenes from Visual Signifiers
- ForceVLA2: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation
- Image Generation as a Visual Planner for Robotic Manipulation

**Efficiency, compression, token / parameter-efficient adaptation for deployment**

token compression, token pruning, quantization, LoRA/adapter merging, KV-cache quantization といった『モデル・推論効率化』や『parameter-efficient fine-tuning』に関する実装寄りの研究が多い。特に multimodal / VLM の推論効率化（token reduction, sparse MoE, mixed-precision kernels）にフォーカスした論文が目立つ。

代表的なタイトル:
- TokenLight: Precise Lighting Control in Images using Attribute Tokens
- DUET-VLM: Dual stage Unified Efficient Token reduction for VLM Training and Inference
- Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization
- MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models
- HAWK: Head Importance-Aware Visual Token Pruning in Multimodal Models

**Robustness, forensics, safety, adversarial attacks and watermarking in generative / multimodal systems**

deepfake/AI-generated detection、watermarking、backdoor/jailbreak攻撃と防御、adversarial clothing／patchesなど、生成系・VLM周りの安全性・検出・防御に関する研究が多く見られる。検証ベンチやchallenge報告も散発的に提出されており実運用リスクへの関心が高い。

代表的なタイトル:
- Omni-Fake: Benchmarking Unified Multimodal Social Media Deepfake Detection
- All in One: Unifying Deepfake Detection, Tampering Localization, and Source Tracing with a Robust Landmark-Identity Watermark
- Phantasia: Context-Adaptive Backdoors in Vision Language Models
- Low-Effort Jailbreak Attacks Against Text-to-Image Safety Filters
- Gaussian Shannon: High-Precision Diffusion Model Watermarking Based on Communication

### 4.2 ホットな細分野

- 3D Gaussian Splatting / 4D reconstruction — 3D/4D gaussian splatting系が目立つ（avatars, dynamic scenes, uncertainty-aware）
- Multimodal Large Language Models / VLMs for spatial & temporal reasoning — MLLM/VLMを空間・時間推論に使う研究が多い
- Diffusion & flow-matching across modalities — diffusion/flow techniques が image/video/motion/3D に広く波及
- Open-vocabulary / zero-shot segmentation & detection — training-free / prototype-based zero-shotが散見される
- Vision-Language-Action and embodied agents — VLA / embodied planning がロボティクス向けに増加
- Token compression & parameter-efficient finetuning (LoRA, adapters) — on-device/latency配慮の研究が多い
- Robustness & forensics of generative models — watermarking, deepfake detection, jailbreak/backdoor対策が多い
- Continual / lifelong learning, federated learning, unlearning — 実運用を見据えた継続学習・プライバシー系が散在

### 4.3 横断的な手法トレンド

- Gaussian Splatting + Neural Rendering hybridization — 3D gaussian splats を NeRF / diffusion / radiance-aware modules と組み合わせる手法が広く使われている
- Diffusion & Flow Matching + Acceleration tricks (linear predictors, Padé, caching) — sampling acceleration と one-step/low-step生成が設計のキーになっている
- Retrieval-augmented / prototype-guided methods for open-vocabulary tasks — retrieval/prototype を使った training-free / few-shot zero-shot 化が定着しつつある
- Token / head / KV-cache compression and adaptive pruning — token pruning, head importance, adaptive KV quantization といった実践的圧縮が横断的に適用されている
- Mixture-of-Experts specialization and routing (MoE-VLMs) — modality-specialized experts とルーティング改善を組み合わせる設計が多い
- Test-time / training-free adaptation and calibration — test-time tuning, post-training calibration, test-time distillation や training-free detectors の採用が目立つ
- Physics- and geometry-aware conditioning (physics-supervised, geometry priors) — physical priors / geometric consistency を明示的に導入する傾向が強い
- Safety / forensic evaluation protocols and benchmark-driven design — evaluation-centric papersやchallenge報告による実運用評価を重視

### 4.4 新しい応用領域

- Animatable high-fidelity 4D / avatar pipelines for telepresence and XR — 3D/4D avatars, face/head avatars, cloth dynamics（telepresence/AR/VRへの応用）
- VLM-guided robotic planning and affordance-conditioned manipulation — vision-language driven planners, affordance grounding for bimanual and dexterous control
- Medical vision-language reasoning and multimodal diagnostics — multimodal VLMs for radiology/whole-slide/echocardiography with emphasis on explainability
- Open-world, online 3D scene editing and simulation-ready asset generation — text/image-to-3D pipelines for simulation and autonomous-driving-ready assets
- Forensic toolchains for generated-media provenance and watermarking — robust watermarking / detection workflows for platform-aware media authentication

### 4.5 意外な観測

- 3D Gaussian Splatting が非常に幅広い応用領域（egocentric reconstruction, avatars, SLAM, aerial-to-ground reconstruction, segmentation）に一気に浸透している点は想定以上に顕著。
- training-free / test-time techniques（training-free segmentation, test-time adaptation, post-training calibration）が生成・認識双方で数多く提案され、学習コストを抑える実装寄りの潮流が強い。
- 安全性関連（jailbreak/backdoor/thermochromic adversarial clothing など）の攻撃研究と同時に、実用的な防御（watermarking, platform-aware evaluation, provenance）が大量に出てきており、“攻防の両面”が同学会で並列に進んでいる。
