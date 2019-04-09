''''
Copyright (c) 2014 - 2015, Hsiaoming Yang

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of the creator nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from mistune import BlockLexer, Renderer, Markdown
import re

class CustomLexer(BlockLexer):
    """
    custom mistune blocklexer
    adds functionality for offset list items
    """
    def parse_list_block(self, m):
        bull = m.group(2)
        # get the list number if starting higher than 1
        off = bull[:-1] if ('.' in bull and int(bull[:-1])>1) else ''
        self.tokens.append({
            'type': 'list_start',
            'ordered': '.' in bull,
            'offset': off,
        })
        self._list_depth += 1
        if self._list_depth > self._max_recursive_depth:
            self.tokens.append({'type': 'list_item_start'})
            self.parse_text(m)
            self.tokens.append({'type': 'list_item_end'})
        else:
            cap = m.group(0)
            self._process_list_item(cap, bull)
        self.tokens.append({'type': 'list_end'})
        self._list_depth -= 1


class ListRenderer(Renderer):
    """
    custom markdown renderer for support offset and task lists
    """
    def list(self, body, offset, ordered=True):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param offset: start offset of the list or None if not present
        :param ordered: whether this list is ordered or not.
        :return String: listblock as HTML
        """
        tag = 'ul'
        if ordered:
            tag = 'ol'
            if isinstance(offset,str) and offset:
                tag += ' start="'+ offset +'"'
        return '<%s>\n%s</%s>\n' % (tag, body, tag)

    def list_item(self, text):
        """
        Rendering list item snippet. Like ``<li>``.
        adds tasklist support
        return: String - listitem as HTML
        """
        checkbox = ""
        # if listitem begins with an [ xX]
        if re.match(r'^\[([ Xx])\]\s(.*)', text):
            # if listitem begins with [ ]
            if re.match(r'^\[([\s])\]',text):
                # checkbox is not checked
                checkbox = '<input disabled="" type="checkbox">'
                # removes [ ] from listitem
                text = text.replace('[ ]','',1)
            # if listitem begins with [x] or [X]
            if re.match(r'^\[([Xx])\]',text):
                # checkbox is checked
                checkbox = '<input checked="" disabled="" type="checkbox">'
                # removes [Xx]
                text = re.sub('\[([Xx])\]','',text,1)
        return '<li>%s%s</li>\n' % (checkbox, text)

class CustomMarkdown(Markdown):
    """
    prep for returning list  as html
    calls custom renderer
    return: String - parsed markdown list as html
    """
    def output_list(self):
        ordered = self.token['ordered']
        off = self.token.get('offset')
        body = self.renderer.placeholder()
        while self.pop()['type'] != 'list_end':
            body += self.tok()
        return self.renderer.list(body, off, ordered)
