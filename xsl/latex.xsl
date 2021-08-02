<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>

    <!-- Normalize whitespace but don't completely trim beginning or end: https://stackoverflow.com/a/5044657/1607849 -->
    <xsl:template match="text()"><xsl:value-of select="translate(normalize-space(concat('&#x7F;',.,'&#x7F;')),'&#x7F;','')"/></xsl:template>

    <xsl:template match="exercise">
\begin{exercise}{<xsl:value-of select="@checkit-slug"/>}{<xsl:value-of select="@checkit-title"/>}{<xsl:value-of select="@checkit-seed"/>}<xsl:apply-templates/>\end{exercise}
</xsl:template>

    <xsl:template match="statement">
\begin{exerciseStatement}<xsl:apply-templates/>\end{exerciseStatement}
</xsl:template>

    <xsl:template match="answer">\begin{exerciseAnswer}<xsl:apply-templates/>\end{exerciseAnswer}
</xsl:template>

    <xsl:template match="p">
<xsl:text>

</xsl:text><xsl:apply-templates/><xsl:text>

</xsl:text>
    </xsl:template>

    <xsl:template match="me">\[<xsl:value-of select="."/>\]</xsl:template>
    <xsl:template match="md">
\begin{align*} <xsl:apply-templates select="mrow"/> \end{align*}
    </xsl:template>
    <xsl:template match="mrow"><xsl:value-of select="."/> \\</xsl:template>
    <xsl:template match="m">\(<xsl:value-of select="."/>\)</xsl:template>

    <xsl:template match="ul">

\begin{itemize}<xsl:apply-templates select="li"/>
\end{itemize}

    </xsl:template>
    <xsl:template match="ol">

\begin{enumerate}[(a)]<xsl:apply-templates select="li"/>
\end{enumerate}

    </xsl:template>
    <xsl:template match="li">
\item <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="c">\verb|<xsl:value-of select="."/>|</xsl:template>
    <xsl:template match="url">\verb|<xsl:value-of select="@href"/>|</xsl:template>

    <xsl:template match="figure">

\begin{figure*}[h]\centering
\includegraphics[height=2in]{assets/<xsl:value-of select="image/@TEMP-assets-file"/>}
\caption*{<xsl:value-of select="caption"/>}
\end{figure*}

    </xsl:template>
    <xsl:template match="image"/><!-- currently kill images outside figures -->

</xsl:stylesheet>