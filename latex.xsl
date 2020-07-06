<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>

    <xsl:template match="statement">

        <xsl:apply-templates/>

    </xsl:template>

    <xsl:template match="answer">

        \textbf{Answer:} <xsl:apply-templates/>

    </xsl:template>

    <xsl:template match="p">

        <xsl:apply-templates/>

    </xsl:template>

    <xsl:template match="me">\[<xsl:value-of select="."/>\]</xsl:template>

    <xsl:template match="md">\[\begin{align*}<xsl:apply-templates select="mrow"/>\end{align*}\]</xsl:template>

    <xsl:template match="mrow"><xsl:value-of select="."/> \\</xsl:template>

    <xsl:template match="m">\(<xsl:value-of select="."/>\)</xsl:template>

    <xsl:template match="ul">\begin{itemize}<xsl:apply-templates select="li"/>\end{itemize}</xsl:template>
    <xsl:template match="ol">\begin{enumerate}[(a)]<xsl:apply-templates select="li"/>\end{enumerate}</xsl:template>
    <xsl:template match="li">\item <xsl:apply-templates/> </xsl:template>

  <!-- https://stackoverflow.com/a/5044657/1607849 -->
  <xsl:template match="text()"><xsl:value-of select="translate(normalize-space(concat('&#x7F;',.,'&#x7F;')),'&#x7F;','')"/></xsl:template>

</xsl:stylesheet>