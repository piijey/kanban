// データ管理
class CorpusViewer {
    constructor() {
        this.data = [];
        this.filteredData = [];
        this.filters = {
            searchText: '',
            searchPictogram: '',
            languages: new Set(),
            /*forms: new Set(),*/
        };
        this.currentModal = null;
        
        // 言語コードから表示名へのマッピング
        this.languageNames = {
            'zh': '中文',
            'zh-Hans': '简体中文',
            'zh-Hant': '繁體中文',
            'ja': '日本語',
            'en': 'English',
            'vi': 'Tiếng Việt',
            'ko': '한국어',
            'de': 'Deutsch',
            'pt': 'Português',
            'ru': 'Русский',
            '_multi': '多言語'
        };
        
        this.init();
    }

    async init() {
        await this.loadData();
        this.buildFilters();
        this.setupEventListeners();
        this.applyFilters();
    }

    async loadData() {
        try {
            const response = await fetch('data.json');
            this.data = await response.json();
        } catch (error) {
            console.error('Failed to load data:', error);
        }
    }

    setupEventListeners() {
        // テキスト検索
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.filters.searchText = e.target.value.toLowerCase();
            this.applyFilters();
        });

        // ピクトグラム検索
        document.getElementById('pictogramInput').addEventListener('input', (e) => {
            this.filters.searchPictogram = e.target.value.toLowerCase();
            this.applyFilters();
        });

        // 言語フィルタ
        document.getElementById('languageSelect').addEventListener('change', (e) => {
            this.filters.languages.clear();
            if (e.target.value) {
                this.filters.languages.add(e.target.value);
            }
            this.applyFilters();
        });

        // 形態フィルタ
        /*
        document.getElementById('formSelect').addEventListener('change', (e) => {
            this.filters.forms.clear();
            if (e.target.value) {
                this.filters.forms.add(e.target.value);
            }
            this.applyFilters();
        });
        */

        // モーダルクローズ
        document.querySelector('.modal-close').addEventListener('click', () => {
            this.closeModal();
        });

        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') {
                this.closeModal();
            }
        });

        // キーボード（Escape）でモーダルクローズ
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.currentModal) {
                this.closeModal();
            }
        });
    }

    buildFilters() {
        const languages = new Set();
        const forms = new Set();

        this.data.forEach(item => {
            item.signs.forEach(sign => {
                sign.language?.forEach(lang => languages.add(lang));
                sign.form?.forEach(form => forms.add(form));
            });
        });

        // 言語セレクト
        const langSelect = document.getElementById('languageSelect');
        Array.from(languages).sort().forEach(lang => {
            const option = document.createElement('option');
            option.value = lang;
            option.textContent = this.languageNames[lang] || lang;
            langSelect.appendChild(option);
        });

        // 形態セレクト
        /*
        const formSelect = document.getElementById('formSelect');
        Array.from(forms).sort().forEach(form => {
            const option = document.createElement('option');
            option.value = form;
            option.textContent = form;
            formSelect.appendChild(option);
        });
        */
    }

    applyFilters() {
        this.filteredData = this.data.filter(item => {
            // テキスト検索
            if (this.filters.searchText) {
                const hasMatch = item.signs.some(sign => 
                    sign.text.toLowerCase().includes(this.filters.searchText)
                );
                if (!hasMatch) return false;
            }

            // ピクトグラム検索
            if (this.filters.searchPictogram) {
                const hasMatch = item.signs.some(sign => 
                    sign.pictograms?.some(p => p.toLowerCase().includes(this.filters.searchPictogram))
                );
                if (!hasMatch) return false;
            }

            // 言語フィルタ
            if (this.filters.languages.size > 0) {
                const hasLanguage = item.signs.some(sign => 
                    sign.language?.some(lang => this.filters.languages.has(lang))
                );
                if (!hasLanguage) return false;
            }

            // 形態フィルタ
            /*
            if (this.filters.forms.size > 0) {
                const hasForm = item.signs.some(sign => 
                    sign.form?.some(form => this.filters.forms.has(form))
                );
                if (!hasForm) return false;
            }
            */

            return true;
        });

        document.getElementById('resultCount').textContent = this.filteredData.length;
        this.renderGallery();
    }

    renderGallery() {
        const gallery = document.getElementById('gallery');
        gallery.innerHTML = '';

        if (this.filteredData.length === 0) {
            gallery.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999; padding: 3rem;">検索結果がありません</p>';
            return;
        }

        this.filteredData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card';

            const languages = new Set();
            item.signs.forEach(sign => {
                sign.language?.forEach(lang => languages.add(lang));
            });

            // テキストプレビュー：各signから2行ずつ取得
            let fullPreview = item.signs.map(s => {
                const lines = s.text.split('\n');
                return lines.slice(0, 2).join('\n');
            }).join('\n');

            card.innerHTML = `
                <img class="card-image" src="${item.image}" alt="${item.id}" loading="lazy">
                <div class="card-content">
                    <p class="card-text">${this.escapeHtml(fullPreview)}</p>
                    <div class="card-tags">
                        ${Array.from(languages).map(lang => `<span class="card-tag">${this.languageNames[lang] || lang}</span>`).join('')}
                    </div>
                </div>
            `;

            card.addEventListener('click', () => this.openModal(item));
            gallery.appendChild(card);
        });
    }

    openModal(item) {
        this.currentModal = item;
        const modal = document.getElementById('modal');

        document.getElementById('modalImage').src = item.image;

        // 全てのsignをリスト表示
        const signsList = document.getElementById('signsList');
        signsList.innerHTML = '';

        item.signs.forEach((sign, idx) => {
            const signDiv = document.createElement('div');
            signDiv.className = `sign-item ${idx > 0 ? 'secondary' : ''}`;

            let signHtml = `<h3>Sign ${idx + 1}</h3>`;
            signHtml += `<div class="sign-text">${this.escapeHtml(sign.text)}</div>`;

            signHtml += `<div class="sign-meta">`;
            signHtml += `<div class="meta-line"><strong>言語:</strong><div class="language-tags">${(sign.language || []).map(lang => `<span class="language-tag">${this.languageNames[lang] || lang}</span>`).join('')}</div></div>`;
            /*
            signHtml += `<div class="meta-line"><strong>形態:</strong><div class="form-tags">${(sign.form || []).map(form => `<span class="form-tag">${form}</span>`).join('')}</div></div>`;
            */
            signHtml += `</div>`;

            if (sign.pictograms && sign.pictograms.length > 0) {
                signHtml += `<div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #e0e0e0;">`;
                signHtml += `<strong style="font-size: 0.8rem; color: #666;">ピクトグラム:</strong>`;
                signHtml += `<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">`;
                signHtml += sign.pictograms.map(p => `<span class="pictogram-tag">${p}</span>`).join('');
                signHtml += `</div></div>`;
            }

            signDiv.innerHTML = signHtml;
            signsList.appendChild(signDiv);
        });

        // 画像のメタデータ
        const imageMeta = document.getElementById('imageMeta');
        imageMeta.innerHTML = `
            <div class="meta-item">
                <div class="info-meta"><strong>撮影日:</strong><div>${item.date ? new Date(item.date).toLocaleDateString('ja-JP') : 'N/A'}</div></div>
                <div class="info-meta"><strong>位置情報:</strong><div>${item.location_info ? [item.location_info.country, item.location_info.province, item.location_info.city, item.location_info.district].filter(v => v).join(', ') : 'N/A'}</div></div>
                <div class="info-meta"><strong>ファイル名:</strong><div>${item.original_image || 'N/A'}</div></div>
                ${item.notes ? `<div class="info-meta"><strong>備考:</strong><div>${item.notes}</div></div>` : ''}
                ${item.link ? `<div class="info-meta"><a href="${item.link}" target="_blank" rel="noopener noreferrer">${item.link}</a></div>` : ''}
            </div>
        `;

        modal.classList.add('active');
    }

    closeModal() {
        document.getElementById('modal').classList.remove('active');
        this.currentModal = null;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    new CorpusViewer();
});
