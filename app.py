        index=len(años_asesor) - 1,
        key="año_historico_asesor"
    )

    base_asesor_hist = df_con_fecha[
        (df_con_fecha["Asesor"] == asesor_historico) &
        (df_con_fecha["Año"] == año_sel_asesor)
    ].copy()

    b1, b2, b3 = st.columns(3)
    b1.metric("Auditorías", len(base_asesor_hist))
    prom_asesor_anual = base_asesor_hist["Puntaje final"].mean()
    b2.metric(
        "Promedio anual del asesor",
        f"{prom_asesor_anual:.1f}%" if pd.notna(prom_asesor_anual) else "Sin datos"
    )
    b3.metric("Campañas", base_asesor_hist["Campaña"].nunique())

    st.markdown("#### Evolución mensual: una línea por campaña")
    asesor_mes_camp = base_asesor_hist.groupby(
        ["Mes", "Campaña"], as_index=False
    ).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values(["Mes", "Campaña"])

    if not asesor_mes_camp.empty:
        fig = px.line(
            asesor_mes_camp, x="Mes", y="Calidad", color="Campaña",
            markers=True, labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
        )
        st.plotly_chart(
            estilo_grafico(
                fig, f"Evolución mensual por campaña | {asesor_historico}",
                "Mes", "Calidad (%)"
            ),
            use_container_width=True
        )

        tabla_asesor_mes = asesor_mes_camp.copy()
        tabla_asesor_mes["Calidad"] = tabla_asesor_mes["Calidad"].round(1)
        mostrar_tabla(tabla_asesor_mes)

    st.markdown("#### Promedio anual por campaña del asesor")
    asesor_por_camp = base_asesor_hist.groupby("Campaña", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values("Calidad", ascending=False)
    asesor_por_camp["Calidad"] = asesor_por_camp["Calidad"].round(1)
    mostrar_tabla(asesor_por_camp)

# =====================================================
# 6. CRITERIOS Y DETALLE DE AUDITORÍAS
# =====================================================
with tab6:
    st.subheader("Análisis general de criterios")
    if not detalle_filtrado.empty:
        resumen_criterios = detalle_filtrado.groupby("Criterio").agg(
            Evaluaciones=("Respuesta", "count"),
            SI=("Respuesta", lambda x: x.isin(["si", "sí"]).sum()),
            NO=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum()),
            NA=("Respuesta", lambda x: (x == "n/a").sum()),
            Descuento=("Descuento", "sum")
        ).reset_index()

        resumen_criterios["% cumplimiento"] = (
            (resumen_criterios["SI"] + resumen_criterios["NA"]) /
            resumen_criterios["Evaluaciones"] * 100
        )
        resumen_criterios["% incumplimiento"] = (
            resumen_criterios["NO"] /
            resumen_criterios["Evaluaciones"] * 100
        )

        mayores = resumen_criterios.sort_values("Descuento", ascending=False)
        fig = px.bar(
            mayores, x="Descuento", y="Criterio", orientation="h",
            labels={"Descuento": "Puntos descontados", "Criterio": "Criterio"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Criterios con mayor descuento", "Puntos", "Criterio"),
            use_container_width=True
        )
        tabla_criterios = resumen_criterios.round(1)
        mostrar_tabla(tabla_criterios)

    st.divider()
    st.subheader("Detalle de auditorías")
    columnas_detalle = [
        "Fecha", "Asesor", "Campaña", "ID", "Tipo de gestión",
        "Tipificación", "Puntaje final", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?", "Tipificación correcta"
    ]
    detalle = filtrado[columnas_detalle].copy()
    detalle["Fecha"] = detalle["Fecha"].dt.strftime("%d/%m/%Y")
    detalle["Puntaje final"] = detalle["Puntaje final"].round(1)
    mostrar_tabla(detalle.sort_values("Fecha", ascending=False))

    csv = filtrado[columnas_detalle].to_csv(
        index=False, sep=";", encoding="utf-8-sig"
    )
    st.download_button(
        "Descargar auditorías en CSV",
        data=csv,
        file_name="auditorias_calidad_contactel.csv",
        mime="text/csv"
    )

# =====================================================
# PIE Y ACTUALIZACIÓN
# =====================================================
st.divider()
st.caption(
    "Calidad y Capacitación | Contactel | "
    "Actualización automática de datos cada 5 minutos."
)
st.caption("La columna AC (Acción) está excluida del análisis y de las vistas.")

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
