# pypodcasts

## 1. Environment setup
Note: I am using fedora as the operating system on my primary development machine. So the instructions are based on Fedora. But similar things exist for all operating systems and can be found easily

### 1.1 Install Poetry
```
sudo dnf install -y poetry
```
### 1.2 Clone the repo
I know that this is expected to be known by most developers. But This is a simple code project and I would like it to be easily understandable for someone who is just starting.
```
git clone https://github.com/nbhirud/pypodcasts.git
```

### 1.3 `poetry install` needed some gpg key. 
Ran the following and selected this key in next step when it prompted. This step will not be needed if you have a gpg key already. You will need to remember the gpg paraphrase for the key you select.

```
gpg --full-generate-key
<!-- gpg2 --full-gen-key -->
```

### 1.4 Install dependencies using poetry:

```
# cd to the repo base directory and run the following
poetry install
```

