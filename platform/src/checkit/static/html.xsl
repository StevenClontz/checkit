<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:stx="https://spatext.clontz.org"
                exclude-result-prefixes="stx">

    <xsl:output method="html" indent="yes"/>

    <!-- Consumer is 'basic' HTML or an LMS: 'canvas', 'd2l', 'moodle' -->
    <xsl:param name="consumer" select="'basic'"/>
    <!-- Subset is 'statement', 'answer', or 'all' -->
    <xsl:param name="subset" select="'all'"/>

    <!-- kill undefined elements -->
    <xsl:template match="*"/>

    <!-- Normalize text() whitespace but don't completely trim beginning or end: https://stackoverflow.com/a/5044657/1607849 -->
    <xsl:template match="text()"><xsl:value-of select="translate(normalize-space(concat('&#x7F;',.,'&#x7F;')),'&#x7F;','')"/></xsl:template>

    <xsl:template match="/">
        <xsl:apply-templates select="stx:exercise"/>
    </xsl:template>

    <xsl:template match="stx:exercise">
        <div>
            <xsl:attribute name="class">
                <xsl:text>checkit exercise</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="data-checkit-slug"><xsl:value-of select="@checkit-slug"/></xsl:attribute>
            <xsl:attribute name="data-checkit-title"><xsl:value-of select="@checkit-title"/></xsl:attribute>
            <xsl:attribute name="data-checkit-seed"><xsl:value-of select="@checkit-seed"/></xsl:attribute>
            <xsl:if test="$subset='statement' or $subset='all'">
                <xsl:apply-templates select="stx:statement"/>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="stx:task">
                    <xsl:if test="$subset='statement' or $subset='all'">
                        <ol>
                            <xsl:apply-templates select="stx:task" mode="statement"/>
                        </ol>
                    </xsl:if>
                    <xsl:if test="$subset='all'">
                        <hr/>
                    </xsl:if>
                    <xsl:if test="$subset='answer' or $subset='all'">
                        <ol>
                            <xsl:apply-templates select="stx:task" mode="answer"/>
                        </ol>
                    </xsl:if>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:if test="$subset='all'">
                        <hr/>
                    </xsl:if>
                    <xsl:if test="$subset='answer' or $subset='all'">
                        <xsl:apply-templates select="stx:answer"/>
                    </xsl:if>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="stx:task" mode="statement">
        <li>
            <xsl:attribute name="class">
                <xsl:text>checkit task</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates select="stx:statement"/>
            <xsl:if test="stx:task">
                <ol>
                    <xsl:apply-templates select="stx:task" mode="statement"/>
                </ol>
            </xsl:if>
        </li>
    </xsl:template>

    <xsl:template match="stx:task" mode="answer">
        <li>
            <xsl:attribute name="class">
                <xsl:text>checkit task</xsl:text>
            </xsl:attribute>
            <xsl:choose>
                <xsl:when test="stx:task">
                    <ol>
                        <xsl:apply-templates select="stx:task" mode="answer"/>
                    </ol>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="stx:answer"/>
                </xsl:otherwise>
            </xsl:choose>
        </li>
    </xsl:template>

    <xsl:template match="stx:statement">
        <div class="checkit statement">
            <xsl:choose>
                <xsl:when test="stx:title">
                    <h4><xsl:value-of select="stx:title"/></h4>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
            <xsl:apply-templates select="stx:p|stx:ul"/>
        </div>
    </xsl:template>

    <xsl:template match="stx:answer">
        <div class="checkit answer">
            <xsl:choose>
                <xsl:when test="stx:title">
                    <h5><xsl:value-of select="stx:title"/></h5>
                </xsl:when>
                <!-- <xsl:otherwise>
                    <h5>Brief Answer:</h5>
                </xsl:otherwise> -->
            </xsl:choose>
            <xsl:apply-templates select="stx:p|stx:ul"/>
        </div>
    </xsl:template>

    <xsl:template match="stx:p">
        <p>
            <xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url"/>
        </p>
    </xsl:template>

    <xsl:template match="stx:ul">
        <ul>
            <xsl:apply-templates select="stx:li"/>
        </ul>
    </xsl:template>
    <xsl:template match="stx:li">
        <li>
            <xsl:if test="stx:title">
                <h6><xsl:value-of select="stx:title"/></h6>
            </xsl:if>
            <xsl:apply-templates select="stx:p|stx:ul"/>
        </li>
    </xsl:template>

    <xsl:template match="stx:m">
        <xsl:choose>
            <xsl:when test="$consumer='canvas'">
                <img>
                    <xsl:attribute name="alt">
                        <xsl:text>LaTeX: </xsl:text>
                        <xsl:value-of select="normalize-space(text())"/>
                    </xsl:attribute>
                    <xsl:attribute name="title">
                        <xsl:text>LaTeX: </xsl:text>
                        <xsl:value-of select="normalize-space(text())"/>
                    </xsl:attribute>
                    <xsl:attribute name="data-latex">
                        <xsl:value-of select="normalize-space(text())"/>
                    </xsl:attribute>
                </img>
            </xsl:when>
            <xsl:otherwise>
                <span class="math math-inline">\(<xsl:value-of select="text()"/>\)</span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="stx:m[@style='display']|stx:me">
        <xsl:choose>
            <xsl:when test="$consumer='canvas'">
                <br/>
                <img>
                    <xsl:attribute name="alt">
                        <xsl:text>LaTeX: </xsl:text>
                        <xsl:value-of select="normalize-space(text())"/>
                    </xsl:attribute>
                    <xsl:attribute name="title">
                        <xsl:text>LaTeX: </xsl:text>
                        <xsl:value-of select="normalize-space(text())"/>
                    </xsl:attribute>
                    <xsl:attribute name="data-latex">
                        <xsl:value-of select="normalize-space(text())"/>
                    </xsl:attribute>
                </img>
                <br/>
            </xsl:when>
            <xsl:otherwise>
                <span class="math math-display">\[<xsl:value-of select="text()"/>\]</span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="stx:em">
        <b><xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url"/></b>
    </xsl:template>

    <xsl:template match="stx:c">
        <code><xsl:value-of select="text()"/></code>
    </xsl:template>

    <xsl:template match="stx:q">
        "<xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url"/>"
    </xsl:template>

    <xsl:template match="stx:url[@href]">
        <a>
            <xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="text()">
                    <xsl:value-of select="text()"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="substring(@href,1,30)"/>
                    <xsl:if test="string-length(@href) &gt; 30">
                        <xsl:text>...</xsl:text>
                    </xsl:if>
                </xsl:otherwise>
            </xsl:choose>
        </a>
    </xsl:template>

</xsl:stylesheet>