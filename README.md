# X-Ray Radiology Report Generation

## Environments and Requirements
This project runs in a Colab environment with the following setup:
- Fine-tuning: Conducted on A100
- Inference: Runs on L4

## Training and Evaluation
Run the following Jupyter Notebook files in Colab for training and evaluation:
- `wanglab_qwen_finetune.ipynb`
- `wanglab_llama_finetune.ipynb`

**Note:** To run the evaluation code, make sure that the `green_score` folder is in the same directory as the notebook files.
  
## Trained Models
You can download trained models here:
- [**Qwen2-VL-7B-Instruct**](https://drive.google.com/drive/folders/10KRZ3oui6HCIMNBbQ1fFlWhUWZWe6SKz?usp=drive_link) (trained with `wanglab_qwen_finetune.ipynb`)  
- [**Llama-3.2-11B-Vision-Instruct**](https://drive.google.com/drive/folders/1-ohCCIXlWGTiYuqkSBojqp48VWwQOd7d?usp=drive_link) (trained with `wanglab_llama_finetune.ipynb`)  

## Results
**Qwen2-VL-7B-Instruct**

| Data Split | Lung | Heart | Mediastinal | Bone |
|----------|----------|----------|----------|----------|
| Validation |  |  |  |  |
| Testing | 0.6327 | 0.8161 | 0.5785 | 0.1002 |


**Llama-3.2-11B-Vision-Instruct**

| Data Split | Lung | Heart | Mediastinal | Bone |
|----------|----------|----------|----------|----------|
| Validation |  |  |  |  |
| Testing | 0.5068 | 0.6943 | 0.4466 | 0.0671 |
